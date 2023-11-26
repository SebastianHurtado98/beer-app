from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from .models import Customer, Beer, Order, Bill
from .serializers import CustomerSerializer, BeerSerializer, OrderSerializer, BillSerializer
from django.db.models import Sum, F

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        ids = self.request.query_params.get('ids')
        if ids:
            ids = ids.split(',')
            queryset = queryset.filter(id__in=ids)
        return queryset

class BeerViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_ids = self.request.query_params.get('customer_ids')
        billed = self.request.query_params.get('billed')

        if customer_ids:
            customer_ids = customer_ids.split(',')
            queryset = queryset.filter(customer_id__in=customer_ids)

        if billed and billed in ['True', 'False']:
            billed = billed == 'True'
            queryset = queryset.filter(billed=billed)

        return queryset
    
class GenerateBillView(views.APIView):
    def post(self, request):
        customer_ids = request.data.get('customer_ids')
        group_type = request.data.get('group', 'IND')
        orders = Order.objects.filter(customer_id__in=customer_ids, billed=False)

        if group_type == 'IND':
            for customer_id in customer_ids:
                total = Order.objects.filter(customer_id=customer_id, billed=False).annotate(
                    total_price=F('beer__price') * F('quantity')
                ).aggregate(total_sum=Sum('total_price'))['total_sum']
                Bill.objects.create(customer_id=customer_id, total=total, paid=False, payment_type='IND')
                orders.filter(customer_id=customer_id).update(billed=True)
            response_data = {'message': 'Facturas individuales creadas exitosamente.'}
        elif group_type == 'GRP':
            total_sum = orders.annotate(total_price=F('beer__price') * F('quantity')).aggregate(total_sum=Sum('total_price'))['total_sum']
            total_per_user = total_sum / len(customer_ids)
            for customer_id in customer_ids:
                Bill.objects.create(customer_id=customer_id, total=total_per_user, paid=False, payment_type='GRP')
                orders.filter(customer_id=customer_id).update(billed=True)
            response_data = {'message': 'Facturas grupales creadas exitosamente.'}
        else:
            return Response({'error': 'Tipo de grupo no válido.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_201_CREATED)

class BillListView(views.APIView):
    def get(self, request):
        queryset = Bill.objects.all()
        customer_ids = self.request.query_params.get('customer_ids')
        paid = self.request.query_params.get('paid')

        if customer_ids:
            customer_ids = customer_ids.split(',')
            queryset = queryset.filter(customer_id__in=customer_ids)

        if paid and paid in ['True', 'False']:
            paid = paid == 'True'
            queryset = queryset.filter(paid=paid)
        serializer = BillSerializer(queryset, many=True)
        return Response(serializer.data)
    

class PayBillView(views.APIView):
    def post(self, request, customer_id):
        bills = Bill.objects.filter(customer_id=customer_id, paid=False)
        if not bills:
            return Response({'message': 'No hay facturas pendientes para el usuario.'}, status=status.HTTP_404_NOT_FOUND)
        bills.update(paid=True)
        return Response({'message': 'Pago realizado exitosamente.'}, status=status.HTTP_200_OK)