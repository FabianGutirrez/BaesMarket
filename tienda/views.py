
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from django.shortcuts import redirect
from tienda.carrito import Carrito
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal
from .models import Producto
from tienda.models import Producto
from tienda.carrito import Carrito
from .carrito import Carrito
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria


def lista_productos(request, categoria_id=None):
    categorias = Categoria.objects.all()

    if categoria_id:
        productos = Producto.objects.filter(categoria_id=categoria_id, disponible=True)
    else:
        productos = Producto.objects.filter(disponible=True)

    productos_destacados = Producto.objects.filter(destacado=True, disponible=True)

    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'productos_destacados': productos_destacados,
        'categorias': categorias
    })



def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria, disponible=True)
    categorias = Categoria.objects.all()
    productos_destacados = Producto.objects.filter(destacado=True)

    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria': categoria,
        'productos_destacados':productos_destacados
    })

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get("cantidad", 1))  # Por defecto 1 si no se envía nada
    carrito = Carrito(request)
    carrito.agregar(producto, cantidad)
    return redirect('ver_carrito')


def ver_carrito(request):
    carrito = Carrito(request)
    productos = carrito.obtener_productos()
    total = carrito.total()
    return render(request, 'tienda/carrito.html', {
        "productos": productos,
        "total": total
    })

def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito(request)
    carrito.eliminar(producto)
    return redirect('ver_carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('ver_carrito')

def quitar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    carrito.quitar(producto_id)
    return redirect('ver_carrito')

def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')





CODIGO_VALIDO = "1234"  # Puedes cambiarlo según tu lógica

def finalizar_compra(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo_qr", "")

        if codigo == CODIGO_VALIDO:
            carrito = Carrito(request)
            resumen = []

            for item in carrito.obtener_productos():
                resumen.append({
                    'nombre': item['nombre'],
                    'cantidad': item['cantidad'],
                    'precio': item['precio'],
                    'subtotal': item['subtotal'],
                    'imagen': item['producto'].imagen.url if item['producto'].imagen else None,
                })

            request.session['compra_realizada'] = {
                'productos': resumen,
                'total': carrito.total()
            }

            carrito.limpiar()

            return redirect('compra_exitosa')
        else:
            messages.error(request, "Código incorrecto. Inténtalo de nuevo.")

    return render(request, 'tienda/finalizar_compra.html')


def compra_exitosa(request):
    datos = request.session.get('compra_realizada')
    if not datos:
        return redirect('lista_productos')
    return render(request, 'tienda/compra_exitosa.html', datos)





def aumentar_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito(request)
    carrito.agregar(producto, cantidad=1)  # Aumenta en 1
    return redirect('ver_carrito')

