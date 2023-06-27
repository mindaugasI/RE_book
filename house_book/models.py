from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image



class Type(models.Model):
    name = models.CharField('Objekto tipas', max_length=20, help_text='Įveskite objekto tipą (pvz. butas)')

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField('Paslaugos pavadinimas', max_length=20, help_text='Įveskite paslaugos pavadinimą (pvz. administravimas)')
    service_description = models.CharField('Paslaugos apibūdinimas', max_length=1000, default='')

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Modelis reprezentuoja paslaugos tiekėją."""
    supp_name = models.CharField('Pavadinimas', max_length=100)
    supp_service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    supp_phone = models.CharField('Telefonas', max_length=20, null=True)
    supp_email = models.EmailField('El. paštas', max_length=50, null=True, db_column='El. paštas')

    def display_service(self):
        return self.supp_service.name

    display_service.short_description = 'Paslaugos pavadinimas'


    class Meta:
        ordering = ['supp_name']

    def get_absolute_url(self):
        """Nurodo konkretaus savininko galinį adresą."""
        return reverse('supplier-detail', args=[str(self.id)])

    def __str__(self):
        """Modelio objekto vaizdavimo eilutė."""
        return f'{self.supp_service} {self.supp_name}'


class Object(models.Model):
    """Modelis reprezentuoja objektą"""
    obj_name = models.CharField('Pavadinimas', max_length=200)
    obj_address = models.CharField('Adresas', max_length=200)
    obj_size = models.FloatField('Plotas', max_length=1000, help_text='Objekto plotas, m2')
    obj_type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)
    obj_description = models.CharField('Aprašymas', max_length=200, default='')
    obj_services = models.ManyToManyField(Service, help_text='Pasirinkite paslaugas objektui')
    obj_suppliers = models.ManyToManyField(Supplier, help_text='Pasirinkite tiekėjus objektui')
    obj_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.obj_name

    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('object-detail', args=[str(self.id)])

    def display_type(self):
        return self.obj_type

    display_type.short_description = 'Objekto tipas'

    def display_supplier(self):
        return self.obj_suppliers


class Owner(models.Model):
    """Modelis reprezentuoja savininką."""
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    obj_owned = models.ManyToManyField(Object, help_text='Pasirinkite objektus')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Nurodo konkretaus savininko galinį adresą."""
        return reverse('owner-detail', args=[str(self.id)])

    def __str__(self):
        """Modelio objekto vaizdavimo eilutė."""
        return f'{self.last_name} {self.first_name}'



class Invoice(models.Model):
    invoice_number = models.CharField('Sąskaitos numeris', max_length=100)
    invoice_date = models.DateField('Sąskaitos data')
    invoice_sum = models.FloatField('Suma', max_length=100)
    invoice_supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True)
    invoice_service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    invoice_object = models.ForeignKey('Object', on_delete=models.SET_NULL, null=True)
    invoice_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS = (('YES', 'Sumokėta'), ('NO', 'Nesumokėta'),)
    invoice_status = models.CharField(max_length=10, choices=STATUS, default='NO', help_text='Sąskaitos statusas')
    def display_status(self):
        return self.invoice_status

    display_status.short_description = 'Apmokėjimo statusas'
    def display_payed(self):
        if self.invoice_status == 'YES':
            return 'APMOKĖTA'
        else:
            return 'NEAPMOKĖTA'

    def display_not_payed(self):
        total = 0
        if self.invoice_status == 'NO':
            total += self.invoice_sum
        return total


    PERIOD = (
        ('01', 'Sausis'),
        ('02', 'Vasaris'),
        ('03', 'Kovas'),
        ('04', 'Balandis'),
        ('05', 'Gegužė'),
        ('06', 'Birželis'),
        ('07', 'Liepa'),
        ('08', 'Rugpjūtis'),
        ('09', 'Rugsėjis'),
        ('10', 'Spalis'),
        ('11', 'Lapkritis'),
        ('12', 'Gruodis'),
    )
    invoice_period = models.CharField(max_length=2, choices=PERIOD, default='01', blank=True, help_text='Paslaugos periodas')
    def display_period(self):
        return self.invoice_period

    display_period.short_description = 'Paslaugos periodas'

    def display_service(self):
        return self.invoice_service

    display_service.short_description = 'Paslaugos pavadinimas'

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = 'Invoices'
        ordering = ['invoice_date']


    def __str__(self):
        return f'{self.invoice_period} - {self.invoice_date} - {self.invoice_service}'

class InvoiceStatus(models.Model):
    status = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
 #   invoice_owner = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return {self.status}

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
