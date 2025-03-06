from django.shortcuts import render
from rest_framework import generics
from .models import LabTest
from .serializer import LabTestSerializer
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import pandas as pd
from io import BytesIO

class LabTestSet(ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

    def perform_create(self, serializer):
        serializer.save()

class LabTestListCreateView(generics.ListCreateAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

class LabTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

class UploadLabTestView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # Get the uploaded file
            file = request.FILES["file"]

            # Read the Excel file
            df = pd.read_excel(file)

            # Validate the file format
            required_columns = ["SERVICES", "COST", "DURATION"]
            if not all(column in df.columns for column in required_columns):
                return JsonResponse(
                    {
                        "error": "Invalid file format. Required columns: SERVICES, COST, DURATION."
                    },
                    status=400,
                )

            # Clean the data
            # Drop rows where all cells are empty
            df = df.dropna(how="all")

            # Drop rows where the COST column is empty
            df = df.dropna(subset=["COST"])

            # Debugging: Log the cleaned DataFrame
            print("Cleaned DataFrame:")
            print(df)

            # Iterate through the rows and update the database
            skipped_rows = []
            for index, row in df.iterrows():
                service = row["SERVICES"]
                cost = row["COST"]
                duration = row["DURATION"]

                # Debugging: Log the row data
                print(f"Processing row {index + 2}: SERVICE='{service}', COST='{cost}', DURATION='{duration}'")

                # Skip rows with missing or invalid cost
                if pd.isna(cost):
                    print(f"Skipping row {index + 2}: Missing cost value")
                    skipped_rows.append(index + 2)  # +2 to account for header and 0-based index
                    continue

                # Convert cost to integer and validate
                try:
                    cost_int = int(cost)  # Convert to integer
                except (ValueError, TypeError):
                    print(f"Skipping row {index + 2}: Invalid cost value '{cost}'")
                    skipped_rows.append(index + 2)
                    continue

                # Ensure cost is not null
                if cost_int is None:
                    print(f"Skipping row {index + 2}: Cost is null")
                    skipped_rows.append(index + 2)
                    continue

                # Debugging: Log the cost value before saving
                print(f"Cost value before saving: {cost_int}")

                # Check if the lab test already exists
                lab_test, created = LabTest.objects.get_or_create(service=service)

                # Update the lab test's cost and duration
                lab_test.cost = cost_int
                lab_test.duration = duration

                # Debugging: Log the lab test instance before saving
                print(f"Lab test instance before saving: {lab_test}")

                # Save the lab test
                lab_test.save()

            # Log skipped rows for debugging
            if skipped_rows:
                print(f"Skipped rows due to missing or invalid cost: {skipped_rows}")

            return JsonResponse(
                {"message": "Lab tests updated successfully!", "skipped_rows": skipped_rows},
                status=200,
            )
        except Exception as e:
            # Log the full error for debugging
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
