# Documentación del Proyecto

## Sistema de Ventas e Inventario - Dashboard Armando

### Información General
- **Framework**: Django 5.2
- **Base de datos**: PostgreSQL
- **Frontend**: Tailwind CSS
- **Autenticación**: Django Auth
- **Despliegue**: Vercel

### Estructura del Proyecto

```
Dashboard_Productos/
├── Apps/
│   ├── templates/           # Plantillas HTML
│   │   ├── index.html      # Layout principal con sidebar
│   │   ├── login.html      # Página de login
│   │   ├── clientes/       # Vistas de clientes
│   │   ├── productos/     # Vistas de productos
│   │   ├── ventas/        # Vistas de ventas
│   │   ├── pagos/         # Vistas de pagos/abonos
│   │   └── paginaciones/  # Componentes de paginación
│   ├── static/
│   │   ├── css/           # Estilos compilados Tailwind
│   │   ├── js/            # Scripts JavaScript
│   │   └── img/           # Imágenes
│   ├── templatetags/      # Filtros personalizados
│   ├── core/              # Módulos core (API dólar BCV)
│   ├── clientes/          # App clientes
│   ├── inventario/        # App productos
│   ├── ventas/           # App ventas
│   ├── abonos/           # App pagos
│   └── views.py          # Vistas principales (login/logout/home)
├── Dashboard_Productos/  # Proyecto Django
├── node/                 # Configuración Tailwind
└── requirements.txt      # Dependencias Python
```

### Modelos de Base de Datos

#### Cliente (`Apps.clientes.models`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Primary Key |
| nombre | CharField(15) | Nombre del cliente |
| apellido | CharField(15, null=True) | Apellido del cliente |
| telefono | BigIntegerField | Teléfono único (11 dígitos) |

#### Producto (`Apps.inventario.models`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Primary Key |
| nombre_producto | CharField(100, unique=True) | Nombre del producto |
| precio_dolar | DecimalField | Precio en dólares |
| cantidad | PositiveIntegerField | Stock disponible |
| imagen | URLField (null=True) | URL de imagen del producto |

#### Venta (`Apps.ventas.models`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Primary Key |
| cliente | ForeignKey(Cliente) | Cliente asociado |
| fecha_venta | DateTimeField | Fecha de venta (auto_now_add) |
| total_pagar | DecimalField | Total a pagar |
| estado | CharField | Estado: PAGADO, PARCIAL_50, PENDIENTE |

#### DetalleVenta (`Apps.ventas.models`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Primary Key |
| venta | ForeignKey(Venta) | Venta asociada |
| producto | ForeignKey(Producto) | Producto vendido |
| cantidad | PositiveIntegerField | Cantidad unidades |
| precio_unitario | DecimalField | Precio unitario |
| subtotal | DecimalField | Subtotal (cantidad × precio) |

#### Pagos (`Apps.abonos.models`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Primary Key |
| numero_factura | CharField(unique=True) | Número de factura (auto-generado: ABON-0001) |
| cliente | ForeignKey(Cliente) | Cliente que paga |
| monto_total | DecimalField | Monto total en bolívares |
| monto_dolar | DecimalField | Monto en dólares |
| fecha | DateTimeField | Fecha del pago |
| body | TextField | Descripción del pago |
| referencia | IntegerField | Referencia bancaria |

#### PagoVenta (`Apps.abonos.models`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Primary Key |
| pago | ForeignKey(Pagos) | Pago asociado |
| venta | ForeignKey(Venta) | Venta pagada |
| monto_aplicado | DecimalField | Monto aplicado a la venta |

### URLs del Proyecto

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/` | login_view | Página de login |
| `/home/` | home | Dashboard principal |
| `/logout/` | logout_view | Cerrar sesión |
| `/clientes/` | listar_clientes | Listar clientes |
| `/clientes/crear/` | crear_cliente | Crear cliente |
| `/clientes/editar/<id>/` | editar_cliente | Editar cliente |
| `/clientes/eliminar/<id>/` | eliminar_cliente | Eliminar cliente |
| `/clientes/buscar/` | busqueda_cliente | Buscar cliente |
| `/productos/` | lista_productos | Listar productos |
| `/productos/crear/` | crear_producto | Crear producto |
| `/productos/editar/<id>/` | editar_producto | Editar producto |
| `/productos/eliminar/<id>/` | eliminar_producto | Eliminar producto |
| `/productos/buscar/` | busqueda_producto | Buscar producto |
| `/ventas/` | lista_ventas | Listar ventas |
| `/ventas/crear/` | crear_venta | Crear venta |
| `/ventas/editar/<id>/` | editar_venta | Editar venta |
| `/ventas/buscar/` | busqueda_venta | Buscar venta |
| `/pagos/` | listado_pagos | Listar pagos |
| `/pagos/crear/` | crear_pago | Registrar pago |
| `/pagos/buscar/` | busqueda_de_pago | Buscar pago |

### API del Dólar BCV
- **Módulo**: `Apps.core.dolar_api`
- **Función**: `valor_obtenido()` - Retorna el valor del dólar BCV desde JSON local

### Configuración de Entorno (.env)
```
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=Dashboard_Datos
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
```

### Paginación
- Clientes: 10 por página
- Productos: 10 por página
- Ventas: 20 por página
- Pagos: 20 por página

### Tecnologías Usadas
- Django 5.2
- PostgreSQL
- Tailwind CSS (vía node)
- SweetAlert2 (notificaciones)
- Font Awesome 6.4 (iconos)
- Flatpickr (calendario)
- WhiteNoise (archivos estáticos en producción)
