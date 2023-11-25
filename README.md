# beer-app
El proyecto es un API para facilitar el pago de cervezas.

Elección del Framework:
Django Rest Framework: Facilita la integración de ORM, autenticación y un admin si son necesarios en el futuro. Si bien estos no se especifican en los requerimientos, queremos que la integración sea sencilla si algo cambia en los requerimientos. 

Supuestos:
Podemos enviar al API el id del cliente. Ya sea que confiemos en que usen su nombre o que el bar tenga integrado algún sistema como pago con pulseras o con algún dispositivo que tenga tu id de cliente. 

Consideraciones:
Si bien no se pide tener la data en una base de datos, dejemos un servicio que permita la integración de cualquier sistema de storage para el futuro.