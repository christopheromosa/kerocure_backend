from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LabTestSale
from .serializers import LabTestSaleSerializer
from django.utils import timezone
from django.db import transaction
from django.db.models import F


class LabTestSaleCreateOrUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        service = request.data.get('service')
        date = request.data.get('date')   # Optional: If not provided, the model's default will be used
        operation_count = request.data.get('operation_count')
        total_amount = request.data.get('total_amount')

        # Set default date if not provided
        if not date:
            date = timezone.now().date()

        # Validate operation_count and total_amount
        try:
            operation_count = int(operation_count)
            total_amount = float(total_amount)
        except (TypeError, ValueError):
            return Response(
                {"error": "operation_count and total_amount must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if a LabTestSale instance already exists for the same service and date
        try:
            lab_test_sale = LabTestSale.objects.get(service=service, date=date)
            # If exists, update the operation_count and total_amount
            lab_test_sale.operation_count = F('operation_count') + operation_count
            lab_test_sale.total_amount = F('total_amount') + total_amount
            lab_test_sale.save()
            lab_test_sale.refresh_from_db()  # Refresh to get updated values
            serializer = LabTestSaleSerializer(lab_test_sale)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LabTestSale.DoesNotExist:
            # If not exists, create a new LabTestSale instance
            serializer = LabTestSaleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class LabTestSaleListView(generics.ListAPIView):
    queryset = LabTestSale.objects.all().order_by("-id")
    serializer_class = LabTestSaleSerializer

class BulkLabTestSaleCreateOrUpdateView(APIView):
        def post(self, request, *args, **kwargs):
            tests = request.data.get('tests', [])  # List of tests to be submitted
            date = request.data.get('date')   # Optional: If not provided, the model's default will be used
            # Set default date if not provided
            if not date:
                date = timezone.now().date()
    
            created_sales = []
            errors = []
    
            with transaction.atomic():  # Use a transaction to ensure atomicity
                for test in tests:
                    service = test.get('service')
                    operation_count = test.get('operation_count', 1)
                    total_amount = test.get('total_amount')
    
                    # Validate operation_count and total_amount
                    try:
                        operation_count = int(operation_count)
                        total_amount = float(total_amount)
                    except (TypeError, ValueError):
                        errors.append({"error": f"Invalid data for service {service}: operation_count and total_amount must be valid numbers."})
                        continue
    
                    # Check if a LabTestSale instance already exists for the same service and date
                    try:
                        lab_test_sale = LabTestSale.objects.get(service=service, date=date)
                        # If exists, update the operation_count and total_amount
                        lab_test_sale.operation_count = F('operation_count') + operation_count
                        lab_test_sale.total_amount = F('total_amount') + total_amount
                        lab_test_sale.save()
                        lab_test_sale.refresh_from_db()  # Refresh to get updated values
                    except LabTestSale.DoesNotExist:
                        # If not exists, create a new LabTestSale instance
                        lab_test_sale = LabTestSale.objects.create(
                            service=service,
                            date=date,  # If date is None, the model's default will be used
                            operation_count=operation_count,
                            total_amount=total_amount,
                        )
                    created_sales.append(lab_test_sale)
    
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    
            # Serialize the created/updated LabTestSale instances
            serializer = LabTestSaleSerializer(created_sales, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
