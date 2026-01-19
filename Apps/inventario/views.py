from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Apps.inventario.models import Producto
from django.core.paginator import Paginator
from django.http import Http404
from Apps.core.dolar_api import valor_obtenido

# Create your views here.

def verificar_datos(request, nombre, precio_dolar, cantidad):
    """Función para verificar los datos del producto"""

    if not nombre or not precio_dolar or not cantidad:
        # Verifica que no seas datos vacios
        messages.error(request, 'Por favor, complete todos los campos.')
        return redirect('productos')
    elif nombre.isnumeric():
        # Verifica que el nombre no contenga números
        messages.error(request, 'El nombre no puede contener números.')
        return redirect('productos')  
    elif not precio_dolar.replace('.', ',', 1) or float(precio_dolar) <= 0:
        # Verifica que el precio sea un número positivo
        messages.error(request, 'El precio debe ser un número positivo.')
        return redirect('productos') 
    elif not cantidad.isdigit() or int(cantidad) < 0:
        # Verifica que la cantidad sea un número entero no negativo
        messages.error(request, 'La cantidad debe ser un número entero no negativo.')
        return redirect('productos') 
    return True


@login_required(login_url='/')
def lista_productos(request):
    """Vista para listar productos"""
    valor = valor_obtenido()

    productos = Producto.objects.all().order_by('id')  # Llamo a todos los productos de la base de datos por orden del identificador
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 10)
        productos = paginator.get_page(page)

    except:
        raise Http404 

    return render(request, 'productos/productos.html', {'productos': productos, 'dolar_bcv': valor})


@login_required(login_url='/')
def crear_producto(request):
    """Vista exclusiva para crear Productos"""

    if request.method == 'POST':
        agregar_producto(request)
        return redirect('productos')

    return redirect('productos')

@login_required(login_url='/')
def agregar_producto(request):
    """Vista para agregar productos"""

    nombre = request.POST.get('nombre').capitalize()
    precio_dolar = request.POST.get('precio')
    cantidad = request.POST.get('cantidad')
    imagen = request.POST.get('imagen')
    
    datos_verificados = verificar_datos(request, nombre, precio_dolar, cantidad)

    if datos_verificados == True:

        try:
            producto = Producto(
                nombre_producto=nombre,
                precio_dolar=precio_dolar,
                cantidad=cantidad,
                imagen=imagen
            )
            producto.save()
            messages.success(request, 'Producto agregado correctamente')
            return
        
        except Exception as e:
            messages.error(request, f'Error al agregar producto: {str(e)}')
            return

    return
    

@login_required(login_url='/')
def editar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        
        if request.method == 'POST':
            nombre_producto = request.POST.get('nombre').capitalize()
            precio_dolar = request.POST.get('precio')
            cantidad = request.POST.get('cantidad')
            
            datos_verificados = verificar_datos(request, nombre_producto, precio_dolar, cantidad)

            if datos_verificados == True:

                producto.nombre_producto = nombre_producto
                producto.precio_dolar = precio_dolar
                producto.cantidad = cantidad

                try:
                    producto.save()
                    messages.success(request, 'Producto actualizado correctamente')
                    return redirect('productos')
                
                except Exception as e:
                    messages.error(request, f'Error al actualizar producto: {str(e)}')
                    return redirect('productos')
        
        return redirect('productos')
    
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe')
        return redirect('productos')

@login_required(login_url='/')
def eliminar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente')
        return redirect('productos')
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe')
        return redirect('productos')
    except Exception as e:
        messages.error(request, f'Error al eliminar el producto: {str(e)}')
        return redirect('productos')
    

@login_required(login_url='/')
def busqueda_producto(request):
    """Vista para buscar productos"""

    dato = request.GET.get('search')

    if dato:
        dato = dato.strip()
        productos = Producto.objects.filter(nombre_producto__icontains=dato)
        # lógica de búsqueda
        
    else:
        messages.error(request, 'No se encontraron productos con ese nombre.')
        return redirect('productos')
    
    if not productos:
        return redirect('productos')
    
    else:
        valor = valor_obtenido()
        return render(request, 'productos/busqueda_producto.html', {
            'productos': productos,
            'dolar_bcv': valor
        })