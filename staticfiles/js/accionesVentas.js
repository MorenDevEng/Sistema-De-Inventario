document.addEventListener('DOMContentLoaded', () => {

    // ===================================================
    // 1. REFERENCIAS GENERALES
    // ===================================================

    const openVentaForm     = document.getElementById('openVentaForm');
    const VentaFormModal   = document.getElementById('VentaFormModal');
    const cancelFormButton = document.getElementById('cancelForm');
    const form             = document.getElementById('formventa');
    const labelCliente     = document.getElementById('dropdownClienteLabel');
    const tbody            = document.querySelector('tbody');

    if (!form) return;

    // ===================================================
    // 2. VARIABLES DE ESTADO (PARA SWAL)
    // ===================================================

    let nombre_cliente   = '';
    let nombre_producto  = [];
    let cantidad_producto = [];
    let precio_producto = [];

    // ===================================================
    // 3. FUNCIONES GENERALES
    // ===================================================

    function abrirModal() {
        VentaFormModal.classList.remove('hidden');
    }

    function cerrarModal() {
        VentaFormModal.classList.add('hidden');
        reseteaFormulario();
    }

    // ===================================================
    // 4. EVENTOS MODAL
    // ===================================================

    openVentaForm.addEventListener('click', abrirModal);
    cancelFormButton.addEventListener('click', cerrarModal);

    // ===================================================
    // 5. EDICIÓN DE VENTA
    // ===================================================

    function llenarFormularioEdicionVenta(compra) {

        compra.productos.forEach((producto, index) => {

            if (index > 0) agregarBtn.click();

            const filas = filasArray();
            const filaActual = filas[index];

            const itemProducto = Array.from(
                filaActual.querySelectorAll('.dropdown-producto-item')
            ).find(item => item.dataset.nombre === producto);

            if (itemProducto) {
                filaActual.querySelector('.dropdown-producto-label').textContent = producto;
                filaActual.querySelector('.producto-id').value = itemProducto.dataset.id;
                filaActual.querySelector('.cantidad-input').value = compra.cantidades[index];
                filaActual.querySelector('.cantidad-input').max = itemProducto.dataset.cantidad;
                precio_producto.push(parseFloat(itemProducto.dataset.precio.replace(',','.')));
                
            };
        });
    }

    tbody.addEventListener('click', (e) => {

        const btnEditar = e.target.closest('.fa-edit');
        if (!btnEditar) return;

        const fila = btnEditar.closest('tr');

        const numeroFactura = fila.querySelector('.factura').textContent.trim();
        const idVenta       = fila.querySelector('.identificador-v').textContent.trim();
        const cliente       = fila.querySelectorAll('td')[1].textContent.trim();
        const fecha         = fila.querySelectorAll('td')[3].textContent.trim();

        const productos  = fila.querySelectorAll('.nombre-producto');
        const cantidades = fila.querySelectorAll('.cantidad-producto');

        const compra = {
            factura: numeroFactura,
            fecha: fecha,
            cliente: cliente,
            productos: Array.from(productos).map(p => p.textContent.trim()),
            cantidades: Array.from(cantidades).map(c => c.textContent.trim())
        };

        document.querySelector('#form-title').innerText = `Editar Venta ${numeroFactura}`;
        form.action = `/ventas/venta/${idVenta}/editar/`;

        campo_editar = document.querySelectorAll('p.text-danger');
        campo_editar.forEach(element => {
            element.classList.add('text-warning');
            element.classList.remove('text-danger');
        });

        labelCliente.textContent = cliente;
        document.getElementById('cliente').value = cliente;

        document.querySelectorAll('.botones-agregar-retirar')
            .forEach(b => b.style.display = 'none');

        abrirModal();
        llenarFormularioEdicionVenta(compra, numeroFactura);

        cancelFormButton.addEventListener('click', () => {
            document.querySelector('#form-title').innerText = 'Registrar Nueva Venta';
            form.action = `/ventas/crear/`; // Restablece la acción para crear nueva venta
            campo_editar.forEach(element => {
                element.classList.add('text-danger');
                element.classList.remove('text-warning');
            });
            labelCliente.textContent = 'Seleccione un cliente...';
            document.getElementById('cliente').value = '';  
            document.querySelectorAll('.botones-agregar-retirar')
                .forEach(b => b.style.display = 'flex');
            llenarFormularioEdicionVenta(compra, {});
            cerrarModal();
        });
    });

    // ===================================================
    // 6. DROPDOWN CLIENTE
    // ===================================================

    const btnCliente  = document.getElementById('dropdownClienteBtn');
    const menuCliente = document.getElementById('dropdownClienteMenu');

    btnCliente.addEventListener('click', (e) => {
        e.stopPropagation();
        menuCliente.classList.toggle('hidden');
    });

    menuCliente.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON') return;

        nombre_cliente = e.target.textContent.trim();
        labelCliente.textContent = nombre_cliente;
        document.getElementById('cliente').value = e.target.id;

        menuCliente.classList.add('hidden');
    });

    document.addEventListener('click', (e) => {
        if (!menuCliente.contains(e.target) && !btnCliente.contains(e.target)) {
            menuCliente.classList.add('hidden');
        }
    });

    // ===================================================
    // 7. PRODUCTOS (FILAS + DROPDOWN)
    // ===================================================

    const container  = document.getElementById('productos-container');
    const agregarBtn = document.querySelector('.agregar-producto');
    const retirarBtn = document.querySelector('.retirar-producto');

    let contadorFilas = 1;

    function limpiarFila(fila) {
        fila.querySelector('.dropdown-producto-label').textContent = 'Producto...';
        fila.querySelector('.producto-id').value = '';
        fila.querySelector('.cantidad-input').value = '';
        fila.querySelector('.dropdown-producto-menu').classList.add('hidden');
    }

    const filasArray = () =>
        Array.from(container.querySelectorAll('.fila-producto'));

    function actualizarEstadoRetirar() {
        retirarBtn.disabled = filasArray().length <= 1;
    }

    container.addEventListener('click', (e) => {

        const toggle = e.target.closest('.dropdown-producto-btn');
        const item   = e.target.closest('.dropdown-producto-item');

        if (toggle) {
            const fila = toggle.closest('.fila-producto');
            const menu = fila.querySelector('.dropdown-producto-menu');

            container.querySelectorAll('.dropdown-producto-menu')
                .forEach(m => {
                    if (m !== menu) {
                        m.classList.add('hidden');
                        m.style.zIndex = '';
                    }
                });

            // Calcular z-index dinámico para que el menú esté por encima de filas inferiores
            const filas = filasArray();
            const idx = filas.indexOf(fila);
            const total = filas.length;
            // Menús en filas superiores reciben mayor z-index: así quedan por encima de las filas añadidas después
            menu.style.zIndex = (100 + (total - idx));
            // Mostrar/ocultar y forzar apertura hacia abajo por defecto
            menu.classList.toggle('hidden');

            // Ajuste: si el menú se sale del viewport por abajo, abrir hacia arriba
            if (!menu.classList.contains('hidden')) {
                const rect = menu.getBoundingClientRect();
                const viewportH = window.innerHeight || document.documentElement.clientHeight;
            }
            return;
        }

        if (item) {
            const fila = item.closest('.fila-producto');
            // Busca el index de la fila que se edito
            const index = filasArray().indexOf(fila);
            // Busca el precio del producto nuevo
            const precio = parseFloat(item.dataset.precio.replace(',', '.'));
            // Agrega el precio al producto
            precio_producto[index] = precio;

            fila.querySelector('.dropdown-producto-label').textContent = item.dataset.nombre;
            fila.querySelector('.producto-id').value = item.dataset.id;
            fila.querySelector('.cantidad-input').max = item.dataset.cantidad;
            fila.querySelector('.dropdown-producto-menu').classList.add('hidden');
        
            
        }

    });

    agregarBtn.addEventListener('click', () => {

        const filas = filasArray();
        const nueva = filas[filas.length - 1].cloneNode(true);

        contadorFilas++;
        nueva.querySelector('.producto-id').id = `producto_${contadorFilas}`;
        nueva.querySelector('.cantidad-input').id = `cantidad_${contadorFilas}`;

        limpiarFila(nueva);
        container.appendChild(nueva);
        actualizarEstadoRetirar();
    });

    retirarBtn.addEventListener('click', () => {

        const filas = filasArray();

        if (filas.length > 1) {
            filas.pop().remove();
        } else {
            limpiarFila(filas[0]);
        }

        actualizarEstadoRetirar();
    });

    // CERRAR MENU SI CLICO AFUERA
    document.addEventListener('click', (e) => {
        if (!container.contains(e.target)) {
            container.querySelectorAll('.dropdown-producto-menu').forEach(m => m.classList.add('hidden'));
        }
    });

    // ===================================================
    // 9. SUBMIT (CAPTURAR DATOS PARA SWAL)
    // ===================================================

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        nombre_producto = [];
        cantidad_producto = [];

        filasArray().forEach(fila => {
            const nombre = fila.querySelector('.dropdown-producto-label').textContent;
            const cantidad = parseInt(fila.querySelector('.cantidad-input').value);

            if (nombre !== 'Producto...' && cantidad) {
                nombre_producto.push(nombre);
                cantidad_producto.push(cantidad);
            }
            
        });

        preguntarGuardarVenta(nombre_cliente, nombre_producto, cantidad_producto, precio_producto, form)
    });

    // ===================================================
    // 9. RESET GENERAL
    // ===================================================

    window.reseteaFormulario = () => {

        filasArray().slice(1).forEach(f => f.remove());
        limpiarFila(filasArray()[0]);

        form.reset();

        nombre_cliente = '';
        nombre_producto = [];
        cantidad_producto = [];
        precio_producto = [];

        labelCliente.textContent = 'Seleccione un cliente...';
        document.getElementById('cliente').value = '';

        menuCliente.classList.add('hidden');
        actualizarEstadoRetirar();
    };

    actualizarEstadoRetirar();

});
