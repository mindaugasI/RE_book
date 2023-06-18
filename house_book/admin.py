from django.contrib import admin
from .models import Type, Service, Object, Owner, Supplier

admin.site.register(Type)
admin.site.register(Service)
admin.site.register(Object)
admin.site.register(Owner)
admin.site.register(Supplier)

