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

    pagos = Pagos.objects.select_related('cliente').prefetch_related('pago_unico__venta__cliente').order_by('-fecha')
    ventas = Venta.objects.select_related('cliente').filter(estado__in=['PARCIAL_50', 'PENDIENTE']).order_by('-fecha_venta')
    detalles = DetalleVenta.objects.select_related('producto').all()

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

    return render(request, 'pagos/pagos.html', {
        'ventas':ventas, 
        'detalles':detalles,
        'clientes_deudores':clientes_deudores, 
        'dolar_bcv':valor, 
        'pagos':pagos
    })

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
        
        monto_dolar = float(monto_dolar)
        monto = float(monto)

        ventas = Venta.objects.select_related('cliente').filter(id__in=ventas_ids, cliente_id=cliente_id)

        if checkbox_pago_total == 'true':

            pago = Pagos(
                cliente_id=cliente_id,
                monto_total=monto,
                body=f'Pago completo para la Venta',
                monto_dolar=monto_dolar,
                referencia=referencia_bancaria
            )
            pago.save()

            pagos_ventas = []
            ids_ventas = []
            for venta in ventas:
                pagos_ventas.append(PagoVenta(
                    pago=pago,
                    venta=venta,
                    monto_aplicado=venta.total_pagar
                ))
                ids_ventas.append(venta.id)
                pago.body += f' #{venta.id}'
            
            PagoVenta.objects.bulk_create(pagos_ventas)
            Venta.objects.filter(id__in=ids_ventas).update(estado='PAGADO')
            pago.save()
                
            messages.success(request, 'Pago registrado correctamente')
            return
                
        else:

            pago = Pagos(
                cliente_id=cliente_id,
                monto_total=monto,
                body=f'Pago del {porc_pagos}% para la Venta',
                referencia=referencia_bancaria
            )
            
            pago.save()

            porc_multi = {'50': 0.5, '100': 1}
            monto_pagar = monto_dolar * porc_multi[porc_pagos]

            pagos_ventas = []
            ids_ventas_parcial = []
            ids_ventas_pagado = []
            nuevos_totales = {}

            for venta in ventas:
                monto_restante = float(venta.total_pagar) - monto_pagar
                pagos_ventas.append(PagoVenta(
                    pago=pago,
                    venta=venta,
                    monto_aplicado=monto
                ))
                pago.body += f' #{venta.id}'
                
                if porc_pagos == '50':
                    ids_ventas_parcial.append(venta.id)
                    nuevos_totales[venta.id] = monto_restante
                elif porc_pagos == '100':
                    ids_ventas_pagado.append(venta.id)

                pago.monto_dolar = monto_pagar
            
            PagoVenta.objects.bulk_create(pagos_ventas)
            
            if ids_ventas_parcial:
                for venta_id in ids_ventas_parcial:
                    Venta.objects.filter(id=venta_id).update(estado='PARCIAL_50', total_pagar=nuevos_totales[venta_id])
            if ids_ventas_pagado:
                Venta.objects.filter(id__in=ids_ventas_pagado).update(estado='PAGADO')
            
            pago.save()
            messages.success(request, 'Pago registrado correctamente')
            return

    return


@login_required(login_url='/')
def busqueda_de_pago(request):
    """Vista para buscar un pago"""

    dato = request.GET.get('dato')

    pagos = Pagos.objects.select_related('cliente').prefetch_related('pago_unico__venta').order_by('-fecha')
    ventas = Venta.objects.select_related('cliente').filter(estado__in=['PARCIAL_50', 'PENDIENTE']).order_by('-fecha_venta')
    detalles = DetalleVenta.objects.select_related('producto').all()

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
        'detalles':detalles,
        'clientes_deudores':clientes_deudores, 
        'dolar_bcv':valor, 
        'pagos':pagos
    })