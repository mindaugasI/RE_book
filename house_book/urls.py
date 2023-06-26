from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('objects/', views.objects, name='objects'),
    path('objects/<int:id>', views.object, name='object'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/<int:id>', views.supplier, name='supplier'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoices/<int:id>', views.invoice, name='invoice'),
    path('services/', views.services, name='services'),
    path('services/<int:id>', views.service, name='service'),
    path('unpayed/', views.unpayed, name='unpayed'),
    path('profile/', views.profile, name='profile'),
]