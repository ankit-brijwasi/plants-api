from django.urls import path
from .views import generate_order, order_complete, view_orders

urlpatterns = [
    path('generate/', generate_order),
    path('complete/', order_complete),
    path('view/', view_orders),
]
