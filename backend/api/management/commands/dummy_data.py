from django.core.management.base import BaseCommand
from api.models import Customer, Beer, Order

class Command(BaseCommand):
    help = 'Poblar la base de datos'

    def handle(self, *args, **options):
        Customer.objects.create(name='Leonardo')
        Customer.objects.create(name='Sebastian')
        Customer.objects.create(name='Mauricio')
        Beer.objects.create(name='Cerveza A', price=10.00)
        Beer.objects.create(name='Cerveza B', price=15.00)
        Beer.objects.create(name='Cerveza C', price=18.00)
        Beer.objects.create(name='Cerveza D', price=20.00)
        for customer in Customer.objects.all():
            for beer in Beer.objects.all()[:2]:
                Order.objects.create(customer=customer, beer=beer, quantity=2, billed=False)
        self.stdout.write(self.style.SUCCESS('Comando ejecutado exitosamente'))
