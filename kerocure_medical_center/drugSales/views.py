from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DrugSale, Drug  # Import the Drug model
from .serializers import DrugSaleSerializer
from django.utils import timezone
from django.db import transaction
from decimal import Decimal 

class DrugSaleCreateOrUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        drug_id = request.data.get('drug')  # Get the drug ID from the request
        date = request.data.get('date', timezone.now().date())
        quantity_sold = request.data.get('quantity_sold')
        total_amount = request.data.get('total_amount')

        # Validate required fields
        if not drug_id or not quantity_sold or not total_amount:
            return Response(
                {"error": "drug, quantity_sold, and total_amount are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate numeric fields
        try:
            quantity_sold = int(quantity_sold)
            total_amount = Decimal(str(total_amount))
        except (ValueError, TypeError):
            return Response(
                {"error": "quantity_sold and total_amount must be numeric"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the Drug object
        try:
            drug = Drug.objects.get(id=drug_id)  # Fetch the Drug object
        except Drug.DoesNotExist:
            return Response(
                {"error": "Drug with the provided ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use atomic transaction to ensure data consistency
        with transaction.atomic():
            try:
                # Try to get an existing DrugSale instance
                drug_sale = DrugSale.objects.get(drug=drug, date=date)
                # If exists, update the quantity_sold and total_amount
                drug_sale.quantity_sold += quantity_sold
                drug_sale.total_amount += total_amount
                drug_sale.save()
                serializer = DrugSaleSerializer(drug_sale)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except DrugSale.DoesNotExist:
                # If not exists, create a new DrugSale instance
                data = {
                    'drug': drug.id,  # Use the ID of the Drug object
                    'date': date,
                    'quantity_sold': quantity_sold,
                    'total_amount': total_amount
                }
                # Pass the drug object into the serializer's context
                serializer = DrugSaleSerializer(data=data, context={'drug': drug})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DrugSaleListView(generics.ListAPIView):
    queryset = DrugSale.objects.all().order_by("-id")
    serializer_class = DrugSaleSerializer
