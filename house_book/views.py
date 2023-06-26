from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Type, Service, Object, Owner, Supplier, Invoice, InvoiceStatus
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect
from .forms import UserUpdateForm, ProfileUpdateForm

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    num_types = Type.objects.count()
    num_services = Service.objects.all().count()
    num_objects = Object.objects.all().count()
    num_owners = Owner.objects.all().count()
    num_suppliers = Supplier.objects.all().count()
    num_invoices = Invoice.objects.all().count()

    # Apsilakymo sesiju skaiciavimas
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Neapmokėtos sąskaitos (tos, kurios turi statusą 'NO')
    num_invoices_unpayed = Invoice.objects.filter(invoice_status__exact='NO').count()

    # Kiek yra šio paskutinio periodo SF
    now = datetime.now().month
    TODAY = '0'+str(now) if len(str(now))==1 else str(now)

    num_invoices_period = Invoice.objects.filter(invoice_period__exact=TODAY).count()

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'num_types': num_types,
        'num_services': num_services,
        'num_objects': num_objects,
        'num_owners': num_owners,
        'num_suppliers': num_suppliers,
        'num_invoices': num_invoices,
        'num_invoices_unpayed': num_invoices_unpayed,
        'num_invoices_period': num_invoices_period,
        'num_visits': num_visits,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą pavadinimą,paslaugą ir objektą.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Invoice.objects.filter(Q(invoice_supplier__supp_name__icontains=query) | Q(invoice_service__name__icontains=query)
                                            | Q(invoice_object__obj_name__icontains=query))
    return render(request, 'search.html', {'invoices': search_results, 'query': query})
# TODO papilvyti foto pridejimo funkcija.

@login_required
def objects(request):
    objects = Object.objects.all()
    context = {
        'objects': objects
    }
    print(objects)
    return render(request, 'objects.html', context=context)

@login_required
def object(request, id):
    single_object = get_object_or_404(Object, pk=id)
    return render(request, 'object.html', {'object': single_object})


def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers
    }
    return render(request, 'suppliers.html', context=context)


def supplier(request, id):
    single_supplier = get_object_or_404(Supplier, pk=id)
    return render(request, 'supplier.html', {'supplier': single_supplier})

@login_required
def invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices.html', {'invoices': invoices})

@login_required
def invoice(request, id):
    single_invoice = get_object_or_404(Invoice, pk=id)
    return render(request, 'invoice.html', {'invoice': single_invoice})

@login_required
def unpayed(request):
    not_payed_invoices = Invoice.objects.all()
    return render(request, 'unpayed.html', {'unpayed': not_payed_invoices})

def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def service(request, id):
    single_service = get_object_or_404(Service, pk=id)
    return render(request, 'service.html', {'service': single_service})


# Registracijos funkcija
@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

