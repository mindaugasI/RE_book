from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Type, Service, Object, Owner, Supplier, Invoice
from datetime import datetime

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    num_types = Type.objects.count()
    num_services = Service.objects.all().count()
    num_objects = Object.objects.all().count()
    num_owners = Owner.objects.all().count()
    num_suppliers = Supplier.objects.all().count()
    num_invoices = Invoice.objects.all().count()

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
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)

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
    suppliers = Supplier.objects.all()
    context = {
        'suppliers':suppliers
    }
    return render(request, 'suppliers.html', context=context)

def supplier(request, id):
    single_supplier = get_object_or_404(Supplier, pk=id)
    return render(request, 'supplier.html', {'supplier': single_supplier})

def invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices.html', {'invoices': invoices})

def invoice(request, id):
    single_invoice = get_object_or_404(Invoice, pk=id)
    return render(request, 'invoice.html', {'invoice': single_invoice})

def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def service(request, id):
    single_service = get_object_or_404(Invoice, pk=id)
    return render(request, 'service.html', {'service': single_service})
