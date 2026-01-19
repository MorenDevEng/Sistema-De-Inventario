// Funcionalidad básica para abrir/cerrar modales 
document.addEventListener('DOMContentLoaded', function() {

    // Intercepta el submit del formulario para confirmar antes de enviar
    const form = document.getElementById('formcliente');
    if (!form) return;
    console.log(form.action);
    
    const nombre = document.getElementById('nombre');
    const apellido = document.getElementById('apellido');
    const prefijo = document.getElementById('prefijo');
    const numero = document.getElementById('numero');
    const telefono = document.getElementById('telefono');

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Detiene el envío normal

        // Combina el prefijo y el número antes de mostrar la alerta
        telefono.value = prefijo.value + numero.value;
        
        preguntarGuardarCliente(nombre.value, apellido.value, telefono.value, form);

    });

    // Abrir formulario de cliente
    document.getElementById('openClientForm').addEventListener('click', function() {

        // Vacia los campos del formulario
        document.querySelector('#clientFormModal #nombre').value = '';
        document.querySelector('#clientFormModal #apellido').value = '';
        document.querySelector('#clientFormModal #numero').value = '';
        
        // Muestra el modal
        document.getElementById('clientFormModal').classList.remove('hidden');
    });
    
    // Cerrar formulario de cliente
    document.getElementById('cancelForm').addEventListener('click', function() {
        document.getElementById('clientFormModal').classList.add('hidden');
    });
});

function MostrarDatosFormulario(DatosNombre, DatosApellido, DatosTelefono) {
    document.querySelector('#clientFormModal #nombre').value = DatosNombre
    document.querySelector('#clientFormModal #apellido').value = DatosApellido
    document.querySelector('#clientFormModal #numero').value = DatosTelefono.slice(3,10)
}

function EditaElCliente(btn, id, nombre, apellido, telefono) {

    document.querySelector('#form-title').innerText = 'Editar Cliente';
    const form = document.getElementById('formcliente');
    console.log(form.action);

    form.action = `/clientes/editarCliente/${id}/`; // Cambia la acción para editar
    console.log(form.action);

    
    campo_editar = document.querySelectorAll('p.text-danger');

    campo_editar.forEach(element => {
        element.classList.add('text-warning');
        element.classList.remove('text-danger');
    });


    document.getElementById('clientFormModal').classList.remove('hidden');

    MostrarDatosFormulario(nombre, apellido, telefono);

    // Cerrar formulario de cliente
    document.getElementById('cancelForm').addEventListener('click', function() {
        document.getElementById('clientFormModal').classList.add('hidden');
        document.querySelector('#form-title').innerText = 'Registrar Nuevo Cliente';
        campo_editar.forEach(element => {
            element.classList.add('text-danger');
            element.classList.remove('text-warning');
            const form = document.getElementById('formcliente');
            form.action = `/clientes/crear/`; // Vacio el action para que vuelva al modo registro
        });
    });

};


function EliminarElCliente(btn, id, nombre, apellido, telefono) {

    preguntarEliminarCliente(id, nombre, apellido, telefono);
};

// Acepta la accion del formulario para la busqueda con el enter
document.getElementById('dato').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {       
        const form = document.getElementById('form_busqueda_cliente');
        // Detener el comportamiento predeterminado si es necesario
        event.preventDefault(); 
        form.submit()
    };
});

// Funcion para combinar el prefijo y el número de teléfono
document.addEventListener('DOMContentLoaded', function() {
const form = document.getElementById('formcliente');
const prefijo = document.getElementById('prefijo');
const numero = document.getElementById('numero');
const telefono = document.getElementById('telefono');

if (!form) return;
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Detiene el envío normal
        // Combina el prefijo y el número antes de enviar
        telefono.value = prefijo.value + numero.value;
        });
});
