from django.contrib import admin
from .models import Cliente
# Register your models here.


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono')
    list_filter = ('nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'telefono')
    list_per_page = 10
