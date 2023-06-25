from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Type, Service, Object, Owner, Supplier, Invoice
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

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

def objects(request):
    objects = Object.objects.all()
    context = {
        'objects': objects
    }
    print(objects)
    return render(request, 'objects.html', context=context)

def object(request, id):
    single_object = get_object_or_404(Object, pk=id)
    return render(request, 'object.html', {'object': single_object})

def suppliers(request):
    paginator = Paginator(Supplier.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_suppliers = paginator.get_page(page_number)
  #  suppliers = Supplier.objects.all()
    context = {
        'suppliers': paged_suppliers
    }
    return render(request, 'suppliers.html', context=context)

def supplier(request, id):
    single_supplier = get_object_or_404(Supplier, pk=id)
    return render(request, 'supplier.html', {'supplier': single_supplier})

def invoices(request):
    paginator = Paginator(Invoice.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_invoices = paginator.get_page(page_number)
#    invoices = Invoice.objects.all()
    return render(request, 'invoices.html', {'invoices': paged_invoices})

def invoice(request, id):
    single_invoice = get_object_or_404(Invoice, pk=id)
    return render(request, 'invoice.html', {'invoice': single_invoice})

def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def service(request, id):
    single_service = get_object_or_404(Service, pk=id)
    return render(request, 'service.html', {'service': single_service})
