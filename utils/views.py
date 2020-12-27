from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from core.models import Cart
from core.serializers import CartSerializer
from nursury.views import IsNursury

User = get_user_model()


@api_view(['POST'])
def generate_order(request):
    cart = get_object_or_404(
        Cart, Q(placed_by=request.user) & Q(status='CART'))
    cart.status = 'ORDERED'
    cart.ordered_on = timezone.now()
    cart.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def order_complete(request):
    cart = get_object_or_404(Cart, pk=request.data.get('pk'))
    cart.status = 'DELIVERED'
    cart.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsNursury])
def view_orders(request):
    orders = Cart.objects.all().prefetch_related('details')

    active_orders = orders.filter(
        Q(details__plant__user=request.user) & Q(status='ORDERED'))
    orders_deliverd = orders.filter(
        Q(details__plant__user=request.user) & Q(status='DELIVERED'))

    active_orders_serializer = CartSerializer(active_orders, many=True)
    orders_deliverd_serializer = CartSerializer(orders_deliverd, many=True)

    return Response(
        {
            'active_orders': active_orders_serializer.data,
            'orders_deliverd': orders_deliverd_serializer.data
        },
        status=status.HTTP_200_OK
    )
