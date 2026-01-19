from django.shortcuts import render, redirect
from .models import Cliente
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.

def verificar_datos_cliente(request, nombre, apellido, telefono):
    """Función para verificar los datos del cliente"""

    if not nombre or not apellido or not telefono:
        # Verifica que no seas datos vacios
        messages.error(request, 'Por favor, complete todos los campos.')
        return redirect('clientes')
    elif nombre.isnumeric() or apellido.isnumeric():
        # Verifica que el nombre y apellido no contengan números
        messages.error(request, 'El nombre y apellido no pueden contener números.')
        return redirect('clientes')  
    elif len(telefono) != 11:
        # Verifica que el teléfono tenga 11 dígitos
        messages.error(request, 'El número de teléfono debe tener 11 dígitos.')
        return redirect('clientes') 
    return True


@login_required(login_url='/')
def crear_cliente(request):
    """Vista exclusiva para crear una Cliente"""

    if request.method == 'POST':
        register_clientes(request)
        return redirect('clientes')

    return redirect('clientes')


@login_required(login_url='/')
def register_clientes(request):
    """Vista para registrar los clientes"""

    # Recibe los datos del formulario de clientes.html
    nombre = request.POST.get('nombre').capitalize()
    apellido = request.POST.get('apellido').capitalize()
    telefono = request.POST.get('telefono')

    # Verifico que los datos sean correctos
    datos_verificados = verificar_datos_cliente(request, nombre, apellido, telefono)
    
    if datos_verificados == True:
        # Al verificar lo anterior guarda los datos en la base de datos
        try:
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono
            )
            messages.success(request, 'El cliente ha sido guardado correctamente')
            return
        except Exception:
            messages.error(request, 'Hubo un error al guardar al cliente')
            return

    return

@login_required(login_url='/')
def listar_clientes(request):
    """Vista para listar los clientes"""

    clientes = Cliente.objects.all().order_by('id')  # Llamo a todos los clientes de la base de datos por orden del identificador
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(clientes, 10)
        clientes = paginator.get_page(page)

    except:
        raise Http404 

    return render(request, 'clientes/clientes.html', {'clientes': clientes} )


@login_required(login_url='/')
def editar_cliente(request, id):
    """Vista para editar los clientes"""

    if request.method == 'POST':
        # Recibe los datos del formulario de clientes.html
        nombre = request.POST.get('nombre').capitalize()
        apellido = request.POST.get('apellido').capitalize()
        telefono = request.POST.get('telefono')

        datos_verificados = verificar_datos_cliente(request, nombre, apellido, telefono)

        if datos_verificados == True:

            # Verifica si el número de teléfono ya existe en otro cliente ay que no se puede repetir
            igualdad_telefono =  Cliente.objects.filter(telefono=telefono).exclude(id=id).exists()
            cliente = Cliente.objects.get(id=id)

            if not igualdad_telefono:
                # Si detecta que el numero no lo tiene ningun cliente, lo guarda, si no, mantiene el mismo
                cliente.telefono = telefono     
            
            cliente.nombre = nombre
            cliente.apellido = apellido 

            cliente.save()

            messages.success(request, 'El cliente ha sido modificado correctamente.')
            return redirect('clientes')
    
    return redirect('clientes')


@login_required(login_url='/')
def eliminar_cliente(request, id):
    """Vista para eliminar los clientes"""

    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    messages.success(request, 'Cliente eliminado satisfactoriamente')
    
    return redirect('clientes')


@login_required(login_url='/')
def busqueda_cliente(request):
    """Vista para buscar el dato en la lista de clientes"""

    dato = request.GET.get("search")

    if dato:

        dato = dato.strip()
        # Busca por teléfono, nombre o apellido (exacto o contiene)
        clientes = Cliente.objects.filter(
            telefono__icontains=dato
        ) | Cliente.objects.filter(
            nombre__icontains=dato
        ) | Cliente.objects.filter(
            apellido__icontains=dato
        )

    else:
        messages.error(request, 'No se encontraron clientes con ese dato.')
        return redirect('clientes')

        
    if clientes.exists():
        return render(request, 'clientes/busqueda_cliente.html', {'clientes': clientes})
    
    else:
        messages.error(request, 'No se encontraron clientes con ese dato.')
        return redirect('clientes')
    

        
        
