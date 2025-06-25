from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'disponible', 'destacado')
    list_filter = ('disponible', 'destacado', 'categoria')
    search_fields = ('nombre',)

admin.site.register(Categoria)
