from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AccountsViewSet

router = DefaultRouter()
router.register(r"accounts", AccountsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
