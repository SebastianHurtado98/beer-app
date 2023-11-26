from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .models import Customer, Beer, Order, Bill
from .serializers import CustomerSerializer, BeerSerializer, OrderSerializer, BillSerializer
from .exceptions import HTTPExceptionUserNotFound, HTTPExceptionBillsNotFound, HTTPExceptionInvalidPaymentTypeGroup, HTTPExceptionCustomerRequired, BillingError
from .services import BillingService

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
        try:
            customer_ids = request.data.get('customer_ids')
            if not customer_ids:
                raise HTTPExceptionCustomerRequired()
            group_type = request.data.get('group', 'IND')
            if group_type not in ['IND', 'GRP']:
                raise HTTPExceptionInvalidPaymentTypeGroup()
            if group_type == 'IND':
                BillingService.create_individual_bills(customer_ids)
                response_data = {'message': 'Facturas individuales creadas exitosamente.'}
            else:
                BillingService.create_group_bills(customer_ids)
                response_data = {'message': 'Facturas grupales creadas exitosamente.'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        except BillingError as e:
            return Response({'error': str(e)}, status=e.status_code)
        except (HTTPExceptionCustomerRequired, HTTPExceptionInvalidPaymentTypeGroup) as e:
            return Response({'error': e.message}, status=e.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PayBillView(views.APIView):
    def post(self, request, customer_id):
        try:
            if not Customer.objects.filter(id=customer_id).exists():
                raise HTTPExceptionUserNotFound()
            bills = Bill.objects.filter(customer_id=customer_id, paid=False)
            if not bills:
                raise HTTPExceptionBillsNotFound()
            bills.update(paid=True)
            return Response({'message': 'Pago realizado exitosamente.'}, status=status.HTTP_200_OK)
        except (HTTPExceptionUserNotFound, HTTPExceptionBillsNotFound) as e:
            return Response({'message': e.message}, status=e.status_code)
        except Exception as e:
            return Response({'message': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
