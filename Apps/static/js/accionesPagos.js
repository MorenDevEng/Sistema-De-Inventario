document.addEventListener('DOMContentLoaded', function() {
    const modalPago = document.getElementById('PagoParcialModal');
    const openPagoModal = document.getElementById('openPagosForm');
    const cancelButtonModal = document.getElementById('cancelFormPago');

    
    openPagoModal.addEventListener('click', () => {
        modalPago.classList.remove('hidden')
        
    });
    
    cancelButtonModal.addEventListener('click', () => {
        resetFormulario()
    });

    // ===================================================
    // 1. DROPDOWN CLIENTE
    // ===================================================

    const labelCliente = document.getElementById('dropdownClienteLabel');
    const btnCliente  = document.getElementById('dropdownClienteBtn');
    const menuCliente = document.getElementById('dropdownClienteMenu');
    let ventasIds = [];
    let subtotal = [];

    btnCliente.addEventListener('click', (e) => {
        e.stopPropagation();
        menuCliente.classList.toggle('hidden');
    });

    menuCliente.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON') return;

        const clienteId = e.target.dataset.id;

        nombre_cliente = e.target.textContent.trim();
        labelCliente.textContent = nombre_cliente;

        if (document.getElementById('cliente').value != clienteId) {
            resetFormularioVentaPorcentaje();
        };

        document.getElementById('cliente').value = clienteId;

        const ventasItems = document.querySelectorAll('.ventas-items');

        ventasItems.forEach((ventas) => {
            if(ventas.dataset.clienteId === clienteId && ventas.dataset.clienteEstado != 'PAGADO'){
                ventas.classList.remove('hidden');
                ventas.closest('div').classList.remove('hidden');
                ventasTotal += parseFloat(ventas.textContent.trim().slice(18).replace(',','.'));
                subtotal.push(parseFloat(ventas.textContent.trim().slice(18).replace(',','.')));
                ventasIds.push(ventas.dataset.ventaId)
                
            } else {
                ventas.classList.add('hidden')
            }
        });

        checkedBoxPagarTodo.removeAttribute('disabled');

        menuCliente.classList.add('hidden');
    });

    document.addEventListener('click', (e) => {
        if (!menuCliente.contains(e.target) && !btnCliente.contains(e.target)) {
            menuCliente.classList.add('hidden');
        };
    });

    // ===================================================
    // 2. DROPDOWN VENTA
    // ===================================================

    const labelVenta = document.getElementById('dropdownVentaLabel');
    const btnVenta  = document.getElementById('dropdownVentaBtn');
    const menuVenta = document.getElementById('dropdownVentaMenu');

    btnVenta.addEventListener('click', (e) => {
        const clienteId = document.getElementById('cliente').value;
        e.stopPropagation();
        
        if (clienteId){
            menuVenta.classList.toggle('hidden');
        }

    });

    menuVenta.addEventListener('click', (e) => {

        if (e.target.tagName !== 'BUTTON') return;

        const ventaId = e.target.dataset.ventaId;
        numero_venta = e.target.textContent.trim();
        labelVenta.textContent = numero_venta;

        if (document.getElementById('venta_pagar').value != ventaId) {
            resetFormPorcentaje()
        };

        document.getElementById('venta_pagar').value = ventaId;    

        if (labelCliente.textContent != 'Seleccione un cliente...' && labelVenta.textContent != 'Seleccione una venta...') {
            porcentajeSeleccionado.removeAttribute('disabled');
            montoTotalPagar.value = '';
            checkedBoxPagarTodo.checked = false;
        };

        menuVenta.classList.add('hidden');
    });

    document.addEventListener('click', (e) => {
        if (!menuVenta.contains(e.target) && !btnVenta.contains(e.target)) {
            menuVenta.classList.add('hidden');
        };
    });



    // ======================================================
    // 3. VISUALIZACION DE LOS PRODUCTOS COMPRADOS POR VENTA
    // ======================================================

    const listaProductos = document.getElementById('productosLista');
    const muestra = document.querySelectorAll('.muestra-productos');


    menuVenta.addEventListener('click', (e) => {
        if (labelVenta != 'Seleccione una venta...'){
            const ventaId = document.getElementById('venta_pagar').value;
            
            if (ventaId) {
                muestra.forEach( (producto) => {
                    if(ventaId === producto.dataset.detallesVenta){
                        producto.classList.remove('hidden')
                        listaProductos.classList.remove('py-6')
                    }
                    else {
                        producto.classList.add('hidden')
                    }
                })
            }

        }   
    });


    // ======================================================
    // 4. PORCENTAJE DE PAGO SELECCIONADO
    // ======================================================

    const porcentajeSeleccionado = document.getElementById('porcentajePago')
    const montoTotalPagar = document.getElementById('montoPago');
    const dolarValor = +(document.querySelector('.monto-dolar').dataset.dolar).replace(',','.');
    const checkedBoxPagarTodo = document.querySelector('[name="bordered-checkbox"]');
    const porcEnviarForm = document.querySelector('[name="porcentaje_seleccionado"]');
    const contenedor_ids_ventas = document.getElementById('venta_pagar');
    const contenedor_ventas = document.querySelector('.bloque-ventas');
    const montoDolar = document.getElementById('montoDolar');
    let inputsVentasCreados = [];
    let ventasTotal = 0;

    // Escuchar cambios en la selección
    porcentajeSeleccionado.addEventListener('change', function() {
        porselec = this.value; // 'El valor de la lista
        
        if (porselec != '') {
            porcentajeMultiplicar = {
                '50':0.5,
                '100':1
            };

            const totalVenta = parseFloat(labelVenta.textContent.slice(18).replace(',','.'));
            calculoVenta = ((totalVenta * porcentajeMultiplicar[porselec]) * dolarValor).toFixed(2);
            
            montoDolar.value = totalVenta;
            montoTotalPagar.value = `Bs. ${calculoVenta}`; 
        
        };

    });

    
    checkedBoxPagarTodo.addEventListener('change', function () {

        // LIMPIAR SIEMPRE ANTES
        limpiarInputsVentas();

        if (checkedBoxPagarTodo.checked) {

            resetFormularioVentaPorcentajeUnicamente();

            calculoVenta = (ventasTotal * dolarValor).toFixed(2);
            montoTotalPagar.value = `Bs. ${calculoVenta}`;
            montoDolar.value = ventasTotal;
            checkedBoxPagarTodo.value = checkedBoxPagarTodo.checked
            
            ventasIds.forEach(ventaId => {

                if (ventasIds[0] == ventaId) {
                    contenedor_ids_ventas.value = ventaId;
                } else {
                    const input = contenedor_ids_ventas.cloneNode(true);
                    input.value = ventaId;

                    contenedor_ventas.appendChild(input);
                    inputsVentasCreados.push(input);
                }

            });


        } else {
            montoTotalPagar.value = '';
            contenedor_ids_ventas.value = '';
            checkedBoxPagarTodo.value = checkedBoxPagarTodo.checked
            montoDolar.value = '';
            
        }
    });

    
    function limpiarInputsVentas() {
        inputsVentasCreados.forEach(input => input.remove());
        inputsVentasCreados = [];
    }

    // ======================================================
    // 5. SUBMIT (DETECCION DE DATOS AL ENVIAR)
    // ======================================================

    const form = document.getElementById('formPagoParcial');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let ventasForm = [];

        const ventasParaEnviar = document.querySelectorAll('#venta_pagar');
        const monto = document.getElementById('montoPago').value;
        const referenciaBancaria = document.getElementById('referenciaBancaria').value;

        if (labelCliente.textContent != 'Seleccione un cliente...') {

            nombre_cliente = labelCliente.textContent;
            ventasParaEnviar.forEach( ventas => {
                ventasForm.push(ventas.value)
            });

            if (checkedBoxPagarTodo.checked) {
                preguntarGuardarPago(nombre_cliente, ventasForm, subtotal, monto, dolarValor, referenciaBancaria, form);
            } else {
                venta = document.querySelector('#venta_pagar').value;
                porcentaje = porcentajeSeleccionado.value;
                total = document.getElementById('montoDolar').value;
                preguntarGuardarPagoConPorcentajes(nombre_cliente, venta, porcentaje, total, monto, referenciaBancaria, form);
            }
        }

        
    })


    // ======================================================
    // 6. EDICION DE ALGUNA FILA DE PAGOS
    // ======================================================

    // const tbody = document.querySelector('tbody');

    // tbody.addEventListener('click', (e) => {
    //     const btnEditar = e.target.closest('.fa-edit');
    //     if (!btnEditar) return;

        
    //     modalPago.classList.remove('hidden')
            
    //     cancelButtonModal.addEventListener('click', () => {
    //         resetFormulario()
    //     });


    // })

    // ======================================================
    // 7. RESET DEL FORMULARIO PARA PORCENTAJE
    // ======================================================

    window.resetFormPorcentaje = () => {
        porcentajeSeleccionado.setAttribute('disabled',true);
        porcentajeSeleccionado.value = '';
        montoTotalPagar.value = '';
        checkedBoxPagarTodo.checked = false;
        checkedBoxPagarTodo.value = checkedBoxPagarTodo.checked;
    };


    // ======================================================
    // 8. RESET DEL FORMULARIO DE VENTA Y PORCENTAJE UNICAMENTE
    // ======================================================

    window.resetFormularioVentaPorcentajeUnicamente = () => {

        // SECCION DE VENTAS
        document.getElementById('dropdownVentaLabel').textContent = 'Seleccione una venta...';
        document.getElementById('venta_pagar').value = '';

        // SECCION DE PORCENTAJES
        porcentajeSeleccionado.setAttribute('disabled',true);
        porcentajeSeleccionado.value = '';
        montoTotalPagar.value = '';
    };



    // ======================================================
    // 9. RESET DEL FORMULARIO DE VENTA Y PORCENTAJE
    // ======================================================

    window.resetFormularioVentaPorcentaje = () => {

        resetFormularioVentaPorcentajeUnicamente();
        // SECCION DE VENTAS
        ventasTotal = 0;
        ventasIds=[];
        subtotal = [];

        montoDolar.value = '';
        listaProductos.classList.add('py-6');
        muestra.forEach((producto) => {
            producto.classList.add('hidden')
        });

        limpiarInputsVentas();

        checkedBoxPagarTodo.checked = false;

    };

    // ======================================================
    // 10. RESET DEL FORMULARIO COMPLETO
    // ======================================================

    window.resetFormulario = () => {

        document.getElementById('dropdownClienteLabel').textContent = 'Seleccione un cliente...';
        document.getElementById('cliente').value = '';

        resetFormularioVentaPorcentaje();

        checkedBoxPagarTodo.setAttribute('disabled',true);

        modalPago.classList.add('hidden');

    };

    window.addEventListener('load', function () {
        // Date Time
        flatpickr('#flatpickr-date-time', {
        enableTime: true,
        dateFormat: 'Y-m-d H:i'
        })
    })
});