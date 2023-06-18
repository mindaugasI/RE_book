from django.db import models
from django.urls import reverse  # Papildome imports


class Type(models.Model):
    name = models.CharField('Objekto tipas', max_length=20, help_text='Įveskite objekto tipą (pvz. butas)')

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField('Paslaugos pavadinimas', max_length=20, help_text='Įveskite paslaugos pavadinimą (pvz. administravimas)')

    def __str__(self):
        return self.name

class Object(models.Model):
    """Modelis reprezentuoja objektą (bet ne specifinį objektą)"""
    obj_name = models.CharField('Pavadinimas', max_length=200)
    obj_address = models.CharField('Adresas', max_length=200)
    obj_size = models.FloatField('Plotas', max_length=1000, help_text='Objekto plotas, m2')
    obj_type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.obj_name

    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('object-detail', args=[str(self.id)])

class Owner(models.Model):
    """Modelis reprezentuoja savininką."""
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Nurodo konkretaus savininko galinį adresą."""
        return reverse('owner-detail', args=[str(self.id)])

    def __str__(self):
        """Modelio objekto vaizdavimo eilutė."""
        return f'{self.last_name} {self.first_name}'


class Supplier(models.Model):
    """Modelis reprezentuoja paslaugos tiekėją."""
    supp_name = models.CharField('Pavadinimas', max_length=100)
    supp_service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['supp_name']

    def get_absolute_url(self):
        """Nurodo konkretaus savininko galinį adresą."""
        return reverse('supplier-detail', args=[str(self.id)])

    def __str__(self):
        """Modelio objekto vaizdavimo eilutė."""
        return f'{self.supp_service} {self.supp_name}'
