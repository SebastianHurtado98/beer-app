from rest_framework.test import APIClient
from django.urls import reverse
from .models import Customer, Beer, Order, Bill
from django.test import TestCase

class PaymentTests(TestCase):
    def setUp(self):
        customer_a = Customer.objects.create(name='Customer A')
        customer_b = Customer.objects.create(name='Customer B')
        beer = Beer.objects.create(name='Beer 1', price=15.00)

        Order.objects.create(customer=customer_a, beer=beer, quantity=2, billed=False)
        Order.objects.create(customer=customer_b, beer=beer, quantity=1, billed=False)

        self.client = APIClient()

    def test_payment_individual_flow(self):
        response = self.client.post(reverse('generate-bill'), {'customer_ids': ['1', '2'], 'group': 'IND'}, format='json')
        self.assertEqual(response.status_code, 201)

        # Verificar bills generados
        bill_a = Bill.objects.get(customer_id=1)
        bill_b = Bill.objects.get(customer_id=2)
        self.assertEqual(bill_a.total, 30.00)
        self.assertEqual(bill_b.total, 15.00)

        # Verificar bills pendientes
        unpaid_bills = Bill.objects.filter(paid=False).count()
        self.assertEqual(unpaid_bills, 2)

        # Realizar pago
        response = self.client.post(reverse('pay-bill', kwargs={'customer_id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('pay-bill', kwargs={'customer_id': 2}))
        self.assertEqual(response.status_code, 200)

        # Verificar bills pendientes
        unpaid_bills = Bill.objects.filter(paid=False).count()
        self.assertEqual(unpaid_bills, 0)

    def test_payment_group_flow(self):
        response = self.client.post(reverse('generate-bill'), {'customer_ids': ['1', '2'], 'group': 'GRP'}, format='json')
        self.assertEqual(response.status_code, 201)

        # Verificar bills generados
        bill_a = Bill.objects.get(customer_id=1)
        bill_b = Bill.objects.get(customer_id=2)
        self.assertEqual(bill_a.total, 22.50)
        self.assertEqual(bill_b.total, 22.50)

        # Verificar bills pendientes
        unpaid_bills = Bill.objects.filter(paid=False).count()
        self.assertEqual(unpaid_bills, 2)

        # Realizar pago
        response = self.client.post(reverse('pay-bill', kwargs={'customer_id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('pay-bill', kwargs={'customer_id': 2}))
        self.assertEqual(response.status_code, 200)

        # Verificar bills pendientes
        unpaid_bills = Bill.objects.filter(paid=False).count()
        self.assertEqual(unpaid_bills, 0)
