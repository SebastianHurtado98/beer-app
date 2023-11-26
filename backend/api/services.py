from api.models import Order, Bill, Customer
from api.exceptions import BillingError
from django.db.models import Sum, F

class BillingService:
    @staticmethod
    def calculate_total_per_customer(customer_id):
        result = Order.objects.filter(customer_id=customer_id, billed=False).annotate(
            total_price=F('beer__price') * F('quantity')
        ).aggregate(total_sum=Sum('total_price'))['total_sum']
        return result if result else 0
    
    @staticmethod
    def validate_customer_ids(customer_ids):
        customers = Customer.objects.filter(id__in=customer_ids)
        if customers.count() != len(customer_ids):
            raise BillingError("Uno o más Customer IDs son inválidos.")

    @staticmethod
    def create_individual_bills(customer_ids):
        try:
            BillingService.validate_customer_ids(customer_ids)
            customers_with_pending_orders = Order.objects.filter(
                customer_id__in=customer_ids, 
                billed=False
            ).values_list('customer_id', flat=True).distinct()
            for customer_id in customers_with_pending_orders:
                total = BillingService.calculate_total_per_customer(customer_id)
                Bill.objects.create(customer_id=customer_id, total=total, paid=False, payment_type='IND')
                Order.objects.filter(customer_id=customer_id).update(billed=True)
        except Exception as e:
            error_message = f"Error al crear facturas individuales. From: {getattr(e, 'message', str(e))}"
            raise BillingError(message=error_message) from e

    @staticmethod
    def create_group_bills(customer_ids):
        try:
            BillingService.validate_customer_ids(customer_ids)
            total_sum = sum(BillingService.calculate_total_per_customer(customer_id) for customer_id in customer_ids)
            if len(customer_ids) == 0:
                raise BillingError("La lista de clientes está vacía.")
            total_per_user = total_sum / len(customer_ids)
            for customer_id in customer_ids:
                Bill.objects.create(customer_id=customer_id, total=total_per_user, paid=False, payment_type='GRP')
                Order.objects.filter(customer_id=customer_id).update(billed=True)
        except Exception as e:
            error_message = f"Error al crear facturas grupales. From: {getattr(e, 'message', str(e))}"
            raise BillingError(message=error_message) from e