from django.shortcuts import render
from rest_framework import generics
from .models import Drug
from .serializers import DrugSerializer
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import pandas as pd
from io import BytesIO
from rest_framework import status
from rest_framework.response import Response

class DrugViewSet(ModelViewSet):
    queryset = Drug.objects.all().order_by("-id")
    serializer_class = DrugSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return Drug.objects.filter(drug_name__icontains=query)

class DrugListCreateView(generics.ListCreateAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

class UploadDrugStockView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # Get the uploaded file
            file = request.FILES["file"]

            # Read the Excel file
            df = pd.read_excel(file)

            # Validate the file format
            required_columns = ["DRUG", "COST", "QUANTITY"]
            if not all(column in df.columns for column in required_columns):
                return JsonResponse(
                    {
                        "error": "Invalid file format. Required columns: Drug, Cost, Quantity."
                    },
                    status=400,
                )

            # Clean the data
            # Drop rows where all cells are empty
            df = df.dropna(how="all")

            # Drop rows where the Cost or Quantity columns are empty
            df = df.dropna(subset=["COST", "QUANTITY"])

            # Debugging: Log the cleaned DataFrame
            print("Cleaned DataFrame:")
            print(df)

            # Iterate through the rows and update the database
            skipped_rows = []
            for index, row in df.iterrows():
                drug_name = row["DRUG"]
                cost = row["COST"]
                quantity = row["QUANTITY"]

                # Debugging: Log the row data
                print(f"Processing row {index + 2}: DRUG='{drug_name}', COST='{cost}', QUANTITY='{quantity}'")

                # Skip rows with missing or invalid cost
                if pd.isna(cost):
                    print(f"Skipping row {index + 2}: Missing cost value")
                    skipped_rows.append(index + 2)  # +2 to account for header and 0-based index
                    continue

                # Skip rows with missing or invalid quantity
                if pd.isna(quantity):
                    print(f"Skipping row {index + 2}: Missing quantity value")
                    skipped_rows.append(index + 2)
                    continue

                # Convert cost to float and validate
                try:
                    cost_float = float(cost)  # Convert to float
                except (ValueError, TypeError):
                    print(f"Skipping row {index + 2}: Invalid cost value '{cost}'")
                    skipped_rows.append(index + 2)
                    continue

                # Convert quantity to integer and validate
                try:
                    quantity_int = int(quantity)  # Convert to integer
                except (ValueError, TypeError):
                    print(f"Skipping row {index + 2}: Invalid quantity value '{quantity}'")
                    skipped_rows.append(index + 2)
                    continue

                # Ensure quantity is non-negative
                if quantity_int < 0:
                    print(f"Skipping row {index + 2}: Quantity must be a positive integer")
                    skipped_rows.append(index + 2)
                    continue

                # Check if the drug already exists
                drug, created = Drug.objects.get_or_create(drug_name=drug_name)

                # Update the drug's cost and quantity
                drug.cost = cost_float
                drug.quantity += quantity_int
                drug.update_status()  # Update the status based on the new quantity
                drug.save()

            # Log skipped rows for debugging
            if skipped_rows:
                print(f"Skipped rows due to missing or invalid data: {skipped_rows}")

            return JsonResponse(
                {"message": "Drug stock updated successfully!", "skipped_rows": skipped_rows},
                status=200,
            )
        except Exception as e:
            # Log the full error for debugging
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)


class DispenseDrugView(APIView):
    def post(self, request, *args, **kwargs):
        drug_id = request.data.get('drug_id')
        quantity_dispensed = request.data.get('quantity_dispensed')

        try:
            drug = Drug.objects.get(id=drug_id)
            drug.dispense_drug(quantity_dispensed)
            drug.save()
            return Response(DrugSerializer(drug).data, status=status.HTTP_200_OK)
        except Drug.DoesNotExist:
            return Response({"error": "Drug not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
