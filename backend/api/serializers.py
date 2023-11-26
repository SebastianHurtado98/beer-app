from rest_framework import serializers
from .models import Customer, Beer, Order, Bill

class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = ['id', 'name', 'price']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'beer', 'quantity', 'billed']

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'customer', 'total', 'paid', 'payment_type']