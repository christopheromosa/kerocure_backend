from django.urls import path
from .views import (
    LabTestSaleCreateOrUpdateView,
    BulkLabTestSaleCreateOrUpdateView,
    LabTestSaleListView,
)

urlpatterns = [
    path('lab-test-sales/', LabTestSaleCreateOrUpdateView.as_view(), name='lab-test-sale-create-or-update'),
    path('lab-test-sales/bulk/', BulkLabTestSaleCreateOrUpdateView.as_view(), name='lab-test-sale-bulk-create-or-update'),
    path('lab-test-sales/list/', LabTestSaleListView.as_view(), name='lab-test-sale-list'),
]
