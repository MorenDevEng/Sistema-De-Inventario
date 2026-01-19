// NOTIFICACIONES SWALALERT2

function mensajeDatosIncorrectos(mensaje) {
    Swal.fire({
    title: "Datos Incorrectos",
    text: mensaje,
    icon: "error",
    confirmButtonText: "Ok!",
    });
};

function mensajeSucces(mensaje) {
    Swal.fire({
    title: "Acción completada",
    text: mensaje,
    icon: "success",
    confirmButtonText: "Ok!",
    });
};  

// SOLICITUD PARA GUARDAR EL CLIENTE
function preguntarGuardarCliente(nombre, apellido, telefono, form) {

    Swal.fire({
        title: "¿Guardara el cliente?",
        html: `
        <div style="text-align: left; max-width: 250px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.6; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="margin-bottom: 12px; color: #1f2937; font-weight: 500;">
                Nombre: <span style="color: #3B82F6; font-weight: bold;">${nombre}</span>
            </div>
            <div style="margin-bottom: 12px; color: #1f2937; font-weight: 500; border-top: 1px solid #d1d5db; padding-top: 8px;">
                Apellido: <span style="color: #3B82F6; font-weight: bold;">${apellido}</span>
            </div>
            <div style="color: #1f2937; font-weight: 500; border-top: 1px solid #d1d5db; padding-top: 8px;">
                Teléfono: <span style="color: #10B981; font-weight: bold;">${telefono}</span>
            </div>
        </div>
        `,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: '#3b6eddff',
        cancelButtonColor: 'rgba(194, 66, 66, 1)',
        confirmButtonText: "Sí, Guardar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit(); // Envía el formulario después de la confirmación
        };
    });
};


// SOLICITUD PARA ELIMINAR EL CLIENTE
function preguntarEliminarCliente (id, nombre, apellido, telefono){

    Swal.fire({
        title: "¿Esta seguro de liminar al cliente?",
        html: `
            <div style="text-align:left; max-width:200px; margin:0 auto;">
                <b>Nombre:</b> ${nombre}<br>
                <b>Apellido:</b> ${apellido}<br>
                <b>Teléfono:</b> ${telefono}
            </div>
        `,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: '#f85830ff',
        cancelButtonColor: 'rgba(88, 91, 223, 1)',
        confirmButtonText: "Sí, Eliminar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/clientes/eliminarCliente/${id}/`;
            
        };
    });
};

// SOLICITUD PARA GUARDAR EL PRODUCTO
function preguntarGuardarProducto(nombre, cantidad, precio, form) {

    Swal.fire({
        title: "¿Desea guardar el Producto?",
        html: `
        <div style="text-align: left; max-width: 350px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.5; background: #f9fafb; border-radius: 8px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="margin-bottom: 10px; padding: 8px; background: #dbeafe; border-radius: 6px; border-left: 4px solid #3B82F6;">
                <strong style="color: #1e40af;">📦 Producto:</strong> ${nombre}
            </div>
            <div style="margin-bottom: 10px; padding: 8px; background: #d1fae5; border-radius: 6px; border-left: 4px solid #10B981;">
                <strong style="color: #065f46;">📊 Stock:</strong> ${cantidad}
            </div>
            <div style="margin-bottom: 10px; padding: 8px; background: #fef3c7; border-radius: 6px; border-left: 4px solid #F59E0B;">
                <strong style="color: #92400e;">💰 Precio:</strong> ${precio} 
            </div>
        </div>
        `,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: '#3b6eddff',
        cancelButtonColor: 'rgba(194, 66, 66, 1)',
        confirmButtonText: "Sí, Guardar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit(); // Envía el formulario después de la confirmación
        };
    });
};

// SOLICITUD PARA ELIMINAR EL PRODUCTO
function preguntarEliminarProducto(id, nombre, cantidad, precio){
    Swal.fire({
    title: "¿Esta seguro de eliminar el Producto?",
    html: `
        <div style="text-align: left; max-width: 350px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.5; background: #fef2f2; border: 2px solid #EF4444; border-radius: 8px; padding: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="margin-bottom: 10px; padding: 8px; background: #fed7d7; border-radius: 6px; border-left: 4px solid #EF4444;">
                <strong style="color: #b91c1c;">🗑️ Producto:</strong> ${nombre}
            </div>
            <div style="margin-bottom: 10px; padding: 8px; background: #fed7d7; border-radius: 6px; border-left: 4px solid #EF4444;">
                <strong style="color: #b91c1c;">📊 Stock:</strong> ${cantidad}
            </div>
            <div style="margin-bottom: 10px; padding: 8px; background: #fef3c7; border-radius: 6px; border-left: 4px solid #F59E0B;">
                <strong style="color: #92400e;">💰 Precio:</strong> ${precio} <span style="color: #dc2626; font-size: 12px;">(Se perderá permanentemente)</span>
            </div>
        </div>
    `,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: '#f85830ff',
    cancelButtonColor: 'rgba(88, 91, 223, 1)',
    confirmButtonText: "Sí, Eliminar",
    cancelButtonText: "Cancelar",
    reverseButtons: true,
    allowOutsideClick: false,

    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/productos/producto/${id}/eliminar/`;
            
        };
    });
};

// SOLICITUD PARA GUARDAR LA VENTA
function preguntarGuardarVenta(cliente, producto, cantidad, precio, form) {
    // Calcular total dinámicamente
    let total = 0;
    for (let i = 0; i < producto.length; i++) {
        total += cantidad[i] * precio[i];
    }

    Swal.fire({
        title: "¿Desea guardar la Venta?",
        html: `
            <div class="text-left space-y-4">
                <div class="flex items-center">
                    <span class="font-medium text-gray-700">Cliente:</span>
                    <span class="text-gray-900 ml-4">${cliente}</span>
                </div>
                
                <div class="border border-gray-300 rounded-md overflow-hidden">
                    <table class="w-full text-sm">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-3 py-2 text-left font-medium text-gray-700">Producto</th>
                                <th class="px-3 py-2 text-center font-medium text-gray-700">Cantidad</th>
                                <th class="px-3 py-2 text-right font-medium text-gray-700">Precio Unit.</th>
                                <th class="px-3 py-2 text-right font-medium text-gray-700">Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${producto.map((prod, i) => `
                                <tr class="border-t border-gray-200">
                                    <td class="px-3 py-2 font-semibold">${prod}</td>
                                    <td class="px-3 py-2 text-center font-semibold">${cantidad[i]}</td>
                                    <td class="px-3 py-2 text-right font-semibold">$${precio[i]}</td>
                                    <td class="px-3 py-2 text-right font-semibold">$${cantidad[i] * precio[i]}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                        <tfoot class="bg-gray-50 border-t border-gray-300">
                            <tr>
                                <td colspan="3" class="px-3 py-2 font-medium text-gray-700 text-right">Total:</td>
                                <td class="px-3 py-2 font-semibold text-gray-900 text-right">$${total}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
                
                <p class="text-xs font-bold text-gray-500">Nota: <span class='text-danger'>Una vez confirmada, la venta se registrará permanentemente.</span></p>
            </div>
        `,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: '#3b6eddff',
        cancelButtonColor: 'rgba(194, 66, 66, 1)',
        confirmButtonText: "Sí, Guardar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit(); // Envía el formulario después de la confirmación
        }
    });
};


// SOLICITUD PARA GUARDAR EL PAGO DE UN CLIENTE

function preguntarGuardarPago(cliente, ventas, subtotal, monto, dolar, referencia, form) {
    Swal.fire({
        title: "¿Desea guardar el Pago?",
        html: `
            <div class="text-left space-y-4">
                <div class="flex items-center">
                    <span class="font-medium text-gray-700">Cliente:</span>
                    <span class="text-gray-900 ml-4">${cliente}</span>
                </div>
                
                <div>
                    <span class="font-medium text-gray-700">Ventas Asociadas:</span>
                    <ul class="mt-2 space-y-1">
                        ${ventas.map((venta, indice)=> `
                            <li class="text-sm text-gray-700 bg-gray-50 px-2 py-1 rounded">
                                Venta #${venta} - Total: $${subtotal[indice]} - Bs. ${(subtotal[indice] * dolar).toFixed(2)}
                            </li>
                        `).join('')}
                    </ul>
                </div>
                
                <div class="flex justify-between items-center border-t border-gray-300 pt-2">
                    <span class="font-semibold text-gray-700">Monto Total a Pagar:</span>
                    <span class="text-lg font-bold text-green-600 ml-4">${monto}</span>
                </div>
                 <div class="flex justify-between items-center col-span-2">
                    <span class="font-medium text-gray-700">Referencia Bancaria:</span>
                    <span class="text-gray-900 font-semibold ml-4">${referencia}</span>
                </div>
                <p class="text-xs text-gray-500">Nota: Una vez confirmado, el pago parcial se registrará permanentemente.</p>
            </div>
        `,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: '#3b6eddff',
        cancelButtonColor: 'rgba(194, 66, 66, 1)',
        confirmButtonText: "Sí, Guardar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit(); // Envía el formulario después de la confirmación
        }
    });
}


function preguntarGuardarPagoConPorcentajes(cliente, venta, porcentaje, total, monto, referencia,form) {
    Swal.fire({
        title: "¿Desea guardar el Pago Parcial con Porcentaje?",
        html: `
            <div class="text-left space-y-4">
                <div class="flex items-center">
                    <span class="font-medium text-gray-700">Cliente:</span>
                    <span class="text-gray-900 ml-4 font-medium">${cliente}</span>
                </div>
                
                <div>
                    <span class="font-medium text-gray-700">Venta Asociada:</span>
                    <div class="text-sm text-gray-700 bg-gray-50 px-2 py-1 rounded mt-2">
                        Venta ${venta} - Total: $${total}
                    </div>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                    <div class="flex justify-between items-center">
                        <span class="font-medium text-gray-700">Porcentaje:</span>
                        <span class="text-gray-900 font-medium">${porcentaje}%</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="font-medium text-gray-700">Total de Venta:</span>
                        <span class="text-gray-900 font-medium">$${total}</span>
                    </div>
                </div>
                    <div class="flex justify-between items-center">
                        <span class="font-medium text-gray-700">Monto a Pagar:</span>
                        <span class="text-lg font-bold text-green-600">${monto}</span>
                    </div>
                    <div class="flex justify-between items-center col-span-2">
                        <span class="font-medium text-gray-700">Referencia Bancaria:</span>
                        <span class="text-gray-900 font-mono ml-4 font-semibold">${referencia}</span>
                    </div
                
                    <p class="text-xs text-gray-500">Nota: Una vez confirmado, el pago parcial se registrará permanentemente.</p>
            </div>
        `,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: '#3b6eddff',
        cancelButtonColor: 'rgba(194, 66, 66, 1)',
        confirmButtonText: "Sí, Guardar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit(); // Envía el formulario después de la confirmación
        }
    });
};
