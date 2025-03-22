from django.urls import path
from .views import DrugSaleCreateOrUpdateView, DrugSaleListView

urlpatterns = [
    path('drug-sales/', DrugSaleCreateOrUpdateView.as_view(), name='drug-sale-create-or-update'),
    path('drug-sales/list/', DrugSaleListView.as_view(), name='drug-sale-list'),
]
