from rest_framework import status

class HTTPExceptionUserNotFound(Exception):
    def __init__(self, message="Usuario no encontrado", status_code=status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class HTTPExceptionBillsNotFound(Exception):
    def __init__(self, message="No hay facturas pendientes para el usuario", status_code=status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class HTTPExceptionInvalidPaymentTypeGroup(Exception):
    def __init__(self, message="No hay facturas pendientes para el usuario", status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class HTTPExceptionCustomerRequired(Exception):
    def __init__(self, message=" Customer IDs son requeridos", status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class BillingError(Exception):
    def __init__(self, message="Error al generar facturas", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)