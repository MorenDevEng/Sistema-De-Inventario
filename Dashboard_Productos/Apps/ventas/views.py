from django.shortcuts import render, redirect
from .models import Venta, DetalleVenta
from django.contrib import messages
from Apps.clientes.models import Cliente
from Apps.inventario.models import Producto
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from Apps.core.dolar_api import valor_obtenido

def verificador_de_datos(request, cliente_id, productos, cantidades):
    """Verifica los datos ingresados para la venta"""

    if not cliente_id or productos == [''] or cantidades == ['']:
        # Verifica que no seas datos vacios
        messages.error(request, 'Por favor, complete todos los campos.')
        return redirect('ventas')
    elif not Cliente.objects.filter(id=cliente_id).exists():
        # Verifica que exista el cliente en la base de datos
        messages.error(request, 'El cliente no existe')
        return redirect('ventas')
    elif True:
        for cantidad in cantidades:
            if int(cantidad) < 0:
                # Verifica que la cantidad comprada sea un número positivo
                messages.error(request, 'La cantidad debe ser positivo y entero.')
                return redirect('ventas') 
    return True

def valor_a_pagar(productos, cantidad):
    valor = []
    for producto in productos:
        prod = Producto.objects.get(id=producto)
        valor.append(prod.precio_dolar)

    valores_productos = [a * b for a, b in zip(valor, cantidad)]

    return sum(valores_productos)

# Create your views here.
@login_required(login_url='/')
def lista_ventas(request):
    """Vista para listar las ventas"""

    valor = valor_obtenido()

    clientes = Cliente.objects.all().order_by('nombre')  # Llamo a todos los clientes por orden de nombre
    detalles = DetalleVenta.objects.all()  # Llamo a todos los detalles de venta
    ventas = Venta.objects.all().order_by('-fecha_venta')  # Llamo a todas las ventas por orden de fecha
    page = request.GET.get('page', 1)
    
    productos = Producto.objects.all().order_by('nombre_producto')  # Llamo a todos los productos por orden de nombre
    try:
        paginator = Paginator(ventas, 20)
        ventas = paginator.get_page(page)

    except:
        raise Http404 
    
    return render(request, 'ventas/ventas.html', {
        'clientes': clientes, 
        'ventas': ventas, 
        'productos': productos, 
        'detalles': detalles, 
        'dolar_bcv':valor})

@login_required(login_url='/')
def crear_venta(request):
    """Vista exclusiva para crear Ventas"""

    if request.method == 'POST':
        agregar_venta(request)
        return redirect('ventas')
    
    return redirect('ventas')

@login_required(login_url='/')
def agregar_venta(request):
    """Vista para agregar una venta"""

    cliente_id = request.POST.get('cliente')
    productos = request.POST.getlist('producto[]')
    cantidades = request.POST.getlist('cantidad[]')

    datos_verificados = verificador_de_datos(request, cliente_id, productos, cantidades)

    if datos_verificados == True:
        # Convierto en enteros los datos dentro de la lista
        cantidades_enteros = [int(cantidad) for cantidad in cantidades]
        # Busco el cliente en la base de datos
        cliente_existente = Cliente.objects.get(id=cliente_id)
        # Busca el total de la venta realizada
        total = valor_a_pagar(productos, cantidades_enteros)
        # Agrupo en una lista el producto y cantidades de c/u
        carrito = [(a, b) for a, b in zip(productos, cantidades)]

        try:
            # Crea la venta
            venta_nueva = Venta(
                cliente=cliente_existente,
                total_pagar=total,     
            )
            venta_nueva.save()
            
            # Crear los detalles
            for item in carrito:

                producto = Producto.objects.get(id=item[0])
                
                detalle = DetalleVenta(
                    venta=venta_nueva,
                    producto=producto,
                    cantidad=int(item[1]),
                    precio_unitario=producto.precio_dolar,
                    subtotal=int(item[1]) * producto.precio_dolar
                )
                detalle.save()
                
                producto.cantidad -= int(item[1])
                producto.save()

            messages.success(request, 'Venta registrada correctamente')
            return

        except Exception as e:
            messages.error(request, f'Error al registrar la venta')
            return
        
    return



@login_required(login_url='/')
def editar_venta(request, venta_id):
    """Vista para editar una venta"""
    cliente = request.POST.get('cliente')
    productos = request.POST.getlist('producto[]')
    cantidades = request.POST.getlist('cantidad[]')

    venta_editar = Venta.objects.get(id=venta_id)

    if cliente.isnumeric(): 
        cliente_id = cliente
    else:
        cliente_id = Cliente.objects.get(nombre=cliente.split(' ')[0], apellido=cliente.split(' ')[1]).id

    datos_verificados = verificador_de_datos(request, cliente_id, productos, cantidades)

    if datos_verificados == True:
        # Convierto en enteros los datos dentro de la lista
        cantidades_enteros = [int(cantidad) for cantidad in cantidades]
        # Busco el cliente en la base de datos
        cliente_existente = Cliente.objects.get(id=cliente_id)
        # Busca el total de la venta realizada
        total = valor_a_pagar(productos, cantidades_enteros)
        # Agrupo en una lista el producto y cantidades de c/u
        carrito = [(a, b) for a, b in zip(productos, cantidades)]

        try:
                # EDITA LA VENTA
                venta_editar.cliente = cliente_existente
                venta_editar.total_pagar = total     
                
                venta_editar.save()
                
                # Crear los detalles
                for indice, item in enumerate(carrito):

                    # OBTENGO EL PRODUCTO A REGISTRAR
                    producto = Producto.objects.get(id=item[0])
                    # OBTENGO A LISTA DE DETALLES A EDITAR
                    detalle_editar = DetalleVenta.objects.filter(venta=venta_editar)[indice]

                    # RESTAURO CANTIDAD DEL PRODUCTO ANTES DE EDITAR
                    producto_reataurar = Producto.objects.get(id=detalle_editar.producto.id)
                    producto_reataurar.cantidad += detalle_editar.cantidad
                    producto_reataurar.save()

                    # EDITO EL DETALLE
                    detalle_editar.producto = producto
                    detalle_editar.cantidad = int(item[1])
                    detalle_editar.precio_unitario = producto.precio_dolar
                    detalle_editar.subtotal = int(item[1]) * producto.precio_dolar
                    detalle_editar.save() 

                    # RESTO LA CANTIDAD DEL PRODUCTO EDITADO
                    producto.cantidad -= int(item[1])
                    producto.save()

                messages.success(request, 'Venta editada correctamente')
                return redirect('ventas')

        except Exception as e:
            messages.error(request, f'Error al editar la venta')
            return redirect('ventas')
            
    return redirect('ventas')




@login_required(login_url='/')
def busqueda_venta(request):
    """Vista para realizar busqueda de una venta"""

    dato = request.GET.get('dato')
    ventas = Venta.objects.all().order_by('-fecha_venta')           # Ordeno las ventas por ultima compra realizada
    clientes = Cliente.objects.all().order_by('nombre')             # Ordeno los clientes por orden alfabetico
    productos = Producto.objects.all().order_by('nombre_producto')  # Ordeno los productos por orden alfabetico
    detalles = DetalleVenta.objects.all()

    if dato:
        
        dato = dato.strip()

        if not dato.isnumeric():

            ventas = ventas.filter(
                cliente__nombre__icontains=dato
            ) | ventas.filter(
                cliente__apellido__icontains=dato
            ) | ventas.filter(
                detalles__producto__nombre_producto__icontains=dato
            ) 

            ventas = ventas.distinct()

        else:

            ventas = ventas.filter(
                cliente__telefono=dato
            )

            ventas = ventas.distinct()
    else:
        messages.error(request, 'No se encontraron ventas asociadas')
        return redirect('ventas')
      
    if not ventas:
        # Si no encuentra en la base de datos regresa con el mensaje de error
        messages.error(request, 'No se encontro una venta con los datos ingresados')
        return redirect('ventas')
    
    else:
        # Si consigue un elemento en la base de datos regresa solo con el valor
        valor = valor_obtenido()
        return render(request, 'ventas/busqueda_venta.html', {
            'ventas':ventas,
            'clientes':clientes,
            'productos':productos,
            'detalles':detalles,
            'dolar_bcv':valor
            })