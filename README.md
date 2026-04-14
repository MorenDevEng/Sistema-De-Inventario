# Sistema de Ventas e Inventario - Dashboard Armando

Dashboard de gestión de ventas, inventario, clientes y pagos desarrollado en Django.

## Características

- **Gestión de Productos**: Crear, editar, eliminar y buscar productos con precios en dólares
- **Gestión de Clientes**: Registro completo de clientes con búsqueda por nombre, apellido o teléfono
- **Sistema de Ventas**: Registro de ventas con múltiples productos, cálculo automático de totales
- **Gestión de Pagos**: Sistema de abonos y pagos parciales con seguimiento de estados
- **Conversión de Moneda**: Integración con API del BCV para conversión Bolívar-Dólar
- **Interfaz Responsive**: Diseño moderno con Tailwind CSS

## Stack Tecnológico

- **Backend**: Django 5.2
- **Base de datos**: PostgreSQL
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Notificaciones**: SweetAlert2
- **Despliegue**: Vercel

## Estructura del Proyecto

```
Dashboard_Productos/
├── Apps/
│   ├── templates/          # Plantillas HTML
│   │   ├── index.html     # Layout principal
│   │   ├── clientes/      # Vistas de clientes
│   │   ├── productos/    # Vistas de productos
│   │   ├── ventas/       # Vistas de ventas
│   │   └── pagos/        # Vistas de pagos
│   ├── static/
│   │   ├── css/           # Estilos Tailwind
│   │   └── js/           # Scripts JavaScript
│   ├── clientes/         # App Django clientes
│   ├── inventario/      # App Django productos
│   ├── ventas/          # App Django ventas
│   ├── abonos/          # App Django pagos
│   └── core/            # Módulos core (API dólar)
├── node/                 # Configuración npm
└── Dashboard_Productos/  # Proyecto Django
```

## Instalación Local

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate    # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno (crear archivo `.env`):
   ```
   SECRET_KEY=tu_secret_key_aqui
   DEBUG=True
   DB_NAME=nombre_db
   DB_USER=usuario
   DB_PASSWORD=password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```

6. Iniciar servidor:
   ```bash
   python manage.py runserver
   ```

## Compilar CSS

Para compilar Tailwind CSS:
```bash
cd node
npm install
npm run tailwind:build
```

## Modelos de Base de Datos

### Cliente
- nombre, apellido, teléfono

### Producto
- nombre_producto, precio_dolar, cantidad, imagen

### Venta
- cliente, fecha_venta, total_pagar, estado

### DetalleVenta
- venta, producto, cantidad, precio_unitario, subtotal

### Pagos
- numero_factura, cliente, monto_total, monto_dolar, fecha, referencia

## Estados de Venta
- `PAGADO`: Venta completamente pagada
- `PARCIAL_50`: Pago del 50% realizado
- `PENDIENTE`: Sin pagos realizados

## Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Login |
| `/home/` | Dashboard |
| `/clientes/` | Listar clientes |
| `/productos/` | Listar productos |
| `/ventas/` | Listar ventas |
| `/pagos/` | Listar pagos |

## Licencia

MIT
