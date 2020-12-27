from django.contrib import admin
from core.models import Order, OrderDetails

admin.site.register(Order)
admin.site.register(OrderDetails)
