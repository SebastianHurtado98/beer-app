# beer-app
El proyecto es un API para facilitar el pago de cervezas.

## Correr el proyecto
Clonar el repositorio.
Para correr el frontend:
- Ir a frontend
- npm install
- npm start

Para correr el api:
- Usar el puerto 8000
- Ir a backend
- Instalar los requerimientos de requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

Poblar con dummy data:
- python manage.py dummy_data

Una vez que tengas dummy data podrás generar un bill:
- POST http://127.0.0.1:8000/api/bills/generate/
- Body: {"customer_ids": [1, 2, 3], "group": "IND"}

O crear nuevas órdenes:
- POST http://127.0.0.1:8000/api/orders/
- Body: {"customer": 3, "beer": 1, "quantity": 1}

Las nuevas órdenes se agregarán a la cuenta grupal si generas el bill:
- POST http://127.0.0.1:8000/api/bills/generate/
- Body: {"customer_ids": [1, 2, 3], "group": "GRP"}

El frontend mostrará el total a pagar pendiente por cada usuario. 
- Usar botón Pay en el frontend.

Correr tests en el backend:
- python manage.py test

## Flujo propuesto

- Las órdenes se crean desde otra interfaz.
- Al momento de pedir la cuenta, el mesero pregunta si lo dividen en partes iguales o individualmente. 
- Desde otra interfaz puedes generar el bill.
- El mesero lleva la interfaz de usuario y solo debe seleccionar su nombre y hacer click en pagar. El usuario verá cuánto debe (sumatoria de sus billings pendientes).

## Stack
- DRF: opté por DRF para facilitar integraciones sencillas en caso de cambios en los requerimientos (autenticación, base de datos, panel administrativo).
- ReactJs: Un SPA con pocos requerimientos se ajusta bien a usar react puro. 
- Base de datos: Para agilizar mi desarrollo y validar el concepto rápidamente, elegí SQLite como base de datos.

## Supuestos
He asumido que es posible identificar a los clientes mediante un ID.

## TODO
- Agrega documentación al API con Swagger
- Consideraciones para moverlo a producción.
- Optimizar consultas según cómo se vaya a usar el resto de endpoints, a nivel de índices o queries.

## Diseño
### Endpoints de la API
#### Listar Cervezas (GET api/beers/):

Permite ver las cervezas disponibles.
La adición de nuevas cervezas (POST) requiere permisos de administrador.

#### Crear Orden (POST api/orders/):

Registra pedidos, requiere el ID del usuario y de la cerveza.
Admite pedir múltiples unidades de una cerveza.

#### Consultar Órdenes (GET api/orders/id=user1,user2,user3?billed=False):

Muestra las órdenes activas y no facturadas.

#### Generar Factura (POST api/bill/):

Crea cuentas basadas en las órdenes no facturadas de un grupo de usuarios.
Cambia el estado de las órdenes a facturadas.
Opciones actuales: generar 3 facturas iguales o 3 facturas distintas (individuales).

#### Ver Monto de Factura (GET api/bill/id=user1,user2, user3):

Devuelve los bills del usuario o usuarios.
El frontend muestra solo una suma de aquellos pendientes de pago.

#### Realizar Pago (POST api/bill/pay/user_id):

Permite pagar la cuenta o cuentas pendientes por usuario.
Endpoint utilizado por el frontend para ejecutar el pago.
No está integrado a una pasarela de pago.