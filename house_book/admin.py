from django.contrib import admin
from .models import Type, Service, Object, Owner, Supplier, Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('display_period', 'invoice_date', 'invoice_sum', 'display_service')

class ObjectAdmin(admin.ModelAdmin):
    list_display = ('obj_name', 'obj_address', 'display_type')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supp_name', 'display_service')



admin.site.register(Type)
admin.site.register(Service)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Owner)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Invoice, InvoiceAdmin)
