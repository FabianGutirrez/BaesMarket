
from .models import Producto


class Carrito:
    def __init__(self, request):
        self.session = request.session
        self.carrito = self.session.get("carrito", {})


    def agregar(self, producto, cantidad=1):
        id = str(producto.id)
        if id not in self.carrito:
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": cantidad,
                "imagen": producto.imagen.url if producto.imagen else None,
            }
        else:
            self.carrito[id]["cantidad"] += cantidad
        self.guardar()

    def quitar(self, producto_id):
        producto_id = str(producto_id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def guardar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def obtener_productos(self):
        productos = []
        for producto_id, item in self.carrito.items():
            try:
                producto = Producto.objects.get(id=producto_id)
                productos.append({
                    "producto": producto,
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "cantidad": item["cantidad"],
                    "precio": float(item["precio"]),
                    "subtotal": float(item["precio"]) * item["cantidad"],
                    "imagen": item.get("imagen"),
                })
            except Producto.DoesNotExist:
                continue
        return productos

    def total(self):
        return sum(float(p["precio"]) * p["cantidad"] for p in self.carrito.values()) 
    