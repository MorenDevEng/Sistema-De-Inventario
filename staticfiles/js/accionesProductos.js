
document.addEventListener('DOMContentLoaded', function() {
    const openProductFormButton = document.getElementById('openProductForm');

    // Intercepta el submit del formulario para confirmar antes de enviar
    const form = document.getElementById('formproducto');
    if (!form) return;
    
    const nombre = document.getElementById('nombre');
    const cantidad = document.getElementById('cantidad');
    const precio = document.getElementById('precio');
    

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Detiene el envío normal

        // Llama a la función de confirmación con Swal
        preguntarGuardarProducto(nombre.value, cantidad.value, precio.value, form);

    });

    openProductFormButton.addEventListener('click', function() {
        
        // Vacia los campos del formulario
        document.querySelector('#ProductFormModal #nombre').value = '';
        document.querySelector('#ProductFormModal #cantidad').value = '';
        document.querySelector('#ProductFormModal #precio').value = '';
        
        // Abrir formulario de cliente
        document.getElementById('ProductFormModal').classList.remove('hidden');

        // Cerrar formulario de cliente
        document.getElementById('cancelForm').addEventListener('click', function() {
            document.getElementById('ProductFormModal').classList.add('hidden');
        });
    });
});

function MostrarDatosFormulario(DatosNombre, DatosCantidad, DatosPrecio) {
    document.querySelector('#ProductFormModal #nombre').value = DatosNombre
    document.querySelector('#ProductFormModal #cantidad').value = DatosCantidad
    document.querySelector('#ProductFormModal #precio').value = parseFloat(DatosPrecio)
};

// Lógica para los botones de editar
function EditaElProducto(btn, id, nombre, cantidad, precio) {

    
    document.querySelector('#form-title').innerText = 'Editar Producto';
    const form = document.getElementById('formproducto');
    form.action = `/productos/producto/${id}/editar/`; // Cambia la acción para editar
    campo_editar = document.querySelectorAll('p.text-danger');

    campo_editar.forEach(element => {
        element.classList.add('text-warning');
        element.classList.remove('text-danger');
    });

    document.getElementById('ProductFormModal').classList.remove('hidden');

    MostrarDatosFormulario(nombre, cantidad, precio);

    // Cerrar formulario de cliente
    document.getElementById('cancelForm').addEventListener('click', function() {
        document.getElementById('ProductFormModal').classList.add('hidden');
        document.querySelector('#form-title').innerText = 'Registrar Nuevo Producto';
        campo_editar.forEach(element => {
            element.classList.add('text-danger');
            element.classList.remove('text-warning');
            const form = document.getElementById('formproducto');
            form.action = `/productos/crear/`; // Vacio el action para que vuelva al modo registro
        });
    });
};

// Lógica para los botones de eliminar
function EliminarElProducto(btn, id, nombre, cantidad, precio) {

    preguntarEliminarProducto(id, nombre, cantidad, precio);
};




// Acepta la accion del formulario para la busqueda con el enter
document.getElementById('dato').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const form = document.getElementById('form_busqueda_producto');
        // Detener el comportamiento predeterminado si es necesario
        event.preventDefault(); 
        form.submit()
    }
});
