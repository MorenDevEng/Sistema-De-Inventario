from django.shortcuts import render, redirect
from Apps.clientes.models import Cliente
from Apps.ventas.models import Venta, DetalleVenta
from Apps.inventario.models import Producto
from Apps.abonos.models import Pagos, PagoVenta
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from Apps.core.dolar_api import valor_obtenido



# Create your views here.

def verificar_datos(request, cliente, ventas, porcentaje_seleccionado, monto, checkbox, referencia, monto_dolar):

    if not cliente or ventas == [''] or not monto or not referencia or not monto_dolar:
        # Verifica que todos los campos esten rellenados
        messages.error(request, 'Por favor complete todos los campos obligatorios.')
        return redirect('pagos')
    elif checkbox != 'true':
        match porcentaje_seleccionado:
            case '50':
                return True
            case '100':
                return True
            case _:
                messages.error(request, 'Por favor seleccione un porcentaje de pago.')
                return redirect('pagos')

    return True



@login_required(login_url='/')
def listado_pagos(request):
    """Lista todos los pagos registrados"""

    pagos = Pagos.objects.all().order_by('-fecha')
    ventas = Venta.objects.all()
    detalles = DetalleVenta.objects.all()

    ESTADOS_DEUDA=['PARCIAL_50',
                'PENDIENTE']

    clientes_deudores = (
        Cliente.objects
        .filter(ventas_clientes__estado__in=ESTADOS_DEUDA)
        .distinct()
        .order_by('nombre')
    )

    valor = valor_obtenido()

    page = request.GET.get('page', 1)
    
    try:
        paginator = Paginator(pagos, 20)
        pagos = paginator.get_page(page)

    except:
        raise Http404 

    return render(request, 'pagos/pagos.html', {'ventas':ventas, 'clientes_deudores':clientes_deudores, 'detalles':detalles, 'dolar_bcv':valor, 'pagos':pagos})

@login_required(login_url='/')
def crear_pago(request):
    """Vista exclusivamente para crear pagos"""
    
    if request.method == 'POST':
        registrar_abono(request)
        return redirect('pagos')
    
    return redirect('pagos')


@login_required(login_url='/')
def registrar_abono(request):
    """Vista para realizar el registro de los pagos"""

    cliente_id = request.POST.get('cliente')
    ventas_ids = request.POST.getlist('venta_pagar[]')
    porc_pagos = request.POST.get('porcentaje')
    monto = request.POST.get('monto')[4:]
    checkbox_pago_total = request.POST.get('bordered-checkbox')
    referencia_bancaria = request.POST.get('referenciaBancaria')
    monto_dolar = request.POST.get('montoDolar')

    datos_verificados = verificar_datos(request, cliente_id, ventas_ids, porc_pagos, monto, checkbox_pago_total, referencia_bancaria, monto_dolar)

    if datos_verificados == True:
        
        # Transforma el valor a flotante para su manipulacion 
        monto_dolar = float(monto_dolar)
        monto = float(monto)
        # Una vez verificado los datos, solicita informacion en la base de datos
        # Esto no ocurrira si ocurre un error en la verificacion

        ventas = (
            Venta.objects
            .filter(id__in=ventas_ids, cliente_id=cliente_id)
        )

        if checkbox_pago_total == 'true':

            # Crear el pago
            pago = Pagos(
                cliente_id=cliente_id,
                monto_total=monto,
                body=f'Pago completo para la Venta',
                monto_dolar=monto_dolar,
                referencia=referencia_bancaria
            )
            pago.save()

            # Aplicar el pago a las ventas
            for venta in ventas:

                pago_venta = PagoVenta(
                    pago=pago,
                    venta=venta,
                    monto_aplicado=venta.total_pagar
                )
                
                pago_venta.save()

                venta.estado = 'PAGADO'
                venta.save()

                pago.body += f' #{venta.id}'
                pago.save()
                
            messages.success(request, 'Pago registrado correctamente')
            return
                
        else:

            # Crear el pago
            pago = Pagos(
                cliente_id=cliente_id,
                monto_total=monto,
                body=f'Pago del {porc_pagos}% para la Venta',
                referencia=referencia_bancaria
            )
            
            pago.save()

            # Aplicar el pago a las ventas
            for venta in ventas:

                porc_multi = {
                    '50':0.5,
                    '100':1
                }

                monto_pagar = monto_dolar * porc_multi[porc_pagos]
                monto_restante = float(venta.total_pagar) - monto_pagar

                pago_venta = PagoVenta(
                    pago=pago,
                    venta=venta,
                    monto_aplicado=monto
                )
                pago_venta.save()

                pago.body += f' #{venta.id}'
                pago.monto_dolar = monto_pagar
                pago.save()
                
                match porc_pagos:

                    case '50':
                        venta.estado = 'PARCIAL_50'
                        venta.total_pagar = monto_restante
                        venta.save()

                        messages.success(request, 'Pago registrado correctamente')
                        return

                    case '100':
                        venta.estado = 'PAGADO'
                        venta.save()

                        messages.success(request, 'Pago registrado correctamente')
                        return

    return


@login_required(login_url='/')
def busqueda_de_pago(request):
    """Vista para buscar un pago"""

    dato = request.GET.get('dato')

    pagos = Pagos.objects.all().order_by('-fecha')
    ventas = Venta.objects.all()
    detalles = DetalleVenta.objects.all()

    ESTADOS_DEUDA=['PARCIAL_50',
                'PENDIENTE']

    clientes_deudores = (
        Cliente.objects
        .filter(ventas_clientes__estado__in=ESTADOS_DEUDA)
        .distinct()
        .order_by('nombre')
    )

    if dato:
        dato = dato.strip()

        if not dato.isnumeric():

            pagos = pagos.filter(
                cliente__nombre__icontains=dato
            ) | pagos.filter(
                cliente__apellido__icontains=dato
            )

            pagos = pagos.distinct()      

        else:

            pagos = pagos.filter(
                referencia=dato
            ) | pagos.filter(
                cliente__telefono=dato
            )

            pagos = pagos.distinct()      

    else:
        messages.error(request, 'No se encontraron pagos asociadas')
        return redirect('pagos')

    if not pagos:
        messages.error(request,'No se encontro un pago con los datos ingresados')
        return redirect('pagos')

    valor = valor_obtenido()
    return render(request, 'pagos/busqueda_pago.html', {
        'ventas':ventas, 
        'clientes_deudores':clientes_deudores, 
        'detalles':detalles, 
        'dolar_bcv':valor, 
        'pagos':pagos
        })