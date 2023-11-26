# beer-app
El proyecto es un API para facilitar el pago de cervezas.

## Stack
### DRF
He decidido utilizar Django Rest Framework por su eficiente integración con ORM, las capacidades de autenticación y la disponibilidad de un panel administrativo. Aunque estos elementos no son requerimientos actuales de mi proyecto, opté por DRF para facilitar una integración sencilla en caso de futuros cambios en los requerimientos.

### Base de datos
Para agilizar mi desarrollo y validar el concepto rápidamente, elegí SQLite como base de datos. Consideré la opción de almacenar la información en memoria, pero esto requeriría un esfuerzo adicional para desarrollar una interfaz compatible con un ORM, caché o cualquier otro servicio que pudiera necesitar más adelante.

### Supuestos
He asumido que es posible identificar a los clientes mediante un ID, ya sea que utilicen sus nombres o que el establecimiento implemente algún sistema de identificación como pulseras de pago o dispositivos que asignen un ID de cliente único.

## Requerimientos
API rest que incluya 4 endpoints:
- Listar la cerveza disponible
- Recibir una orden
- Obtener la cuenta.
- Pagar la cuenta. La cuenta puede dividirse entre los 3 amigos por igual. Este endpoint también debe permitirle a cada uno pagar lo que ordenó.

Frontend:
- PR donde se implemente la interfaz de pago.
- Esta solo debe incluir un botón, un dropdown con la lista de los amigos y el valor a pagar.

Consideraciones adicionales:
- Agrega un par de unit tests que consideres claves e incluye un readme con instrucciones para ejecutar el código
- Dummy data debería incluir solo este caso (3 amigos en un bar).
- Agregar instrucciones de cómo correr el proyecto.

Nice to have:
- Agrega documentación al API.
- Consideraciones para moverlo a producción.
- Optimizar consultas según cómo se vaya a usar el resto de endpoints.

## Diseño
### Endpoints de la API
#### Listar Cervezas (GET api/beers/):

Permite ver las cervezas disponibles.
La adición de nuevas cervezas (POST) requiere permisos de administrador.

#### Crear Orden (POST api/orders/):

Registra pedidos, requiere el ID del usuario y de la cerveza.
Admite pedir múltiples unidades de una cerveza.

#### Consultar Órdenes (GET api/orders/id=[user1, user2, user3]?billed=False):

Muestra las órdenes activas y no facturadas para calcular la cuenta.
Diferencia entre órdenes activas y pagadas.

#### Generar Factura (POST api/bill/):

Crea cuentas basadas en las órdenes no facturadas de un grupo de usuarios.
Cambia el estado de las órdenes a facturadas.
Opciones actuales: generar 3 facturas iguales o 3 facturas distintas.

#### Ver Monto de Factura (GET api/bill/id=[user1, user2, user3]):

Devuelve el total a pagar, sumando las facturas pendientes del usuario.
Utilizado por el frontend para mostrar el monto a pagar.

#### Realizar Pago (POST api/bill/pay/user_id):

Permite cancelar la cuenta o cuentas pendientes por usuario.
Endpoint utilizado por el frontend para ejecutar el pago.

### Consideraciones:
Vas a un bar, sueles pedir X cervezas. Tendrías que limitar la cantidad de cerveza por cada uno siempre. 
Dado que el problema es que uno siempre toma mucho más y no paga, supongamos que se quieren dar el trabajo de asignarse las cervezas siempre.

## Flujo propuesto

- Las órdenes se crean desde otra interfaz, por el mesero quizás.
- Al momento de pedir la cuenta, el mesero pregunta si lo dividen en partes iguales o individualmente. Otras opciones aún no son habilitadas.
- El mesero lleva la interfaz de usuario y solo debe seleccionar su nombre y hacer click en pagar. El usuario verá cuánto debe (sumatoria de sus billings pendientes).