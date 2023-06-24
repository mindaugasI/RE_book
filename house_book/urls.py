from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('objects/', views.objects, name='objects'),
    path('objects/<int:id>', views.object, name='object'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/<int:id>', views.supplier, name='supplier'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoices/<int:id>', views.invoice, name='invoice'),
    path('services/', views.services, name='services'),
    path('services/<int:id>', views.service, name='service'),
]