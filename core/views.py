from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializer

from core import models, serializers


class CartAPIView(APIView):
    '''
    GENERATE USER'S CART

    ALLOWED METHODS: GET, PUT, DELETE
    '''

    def get(self, request):
        orders = get_object_or_404(models.Cart, Q(
            placed_by=request.user) & Q(status='CART'))
        serializer = serializers.CartSerializer(orders, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        data = {**request.data}
        data.update({'placed_by': {'email': request.user.email}})

        serializer = serializers.CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = get_object_or_404(models.Cart, placed_by=request.user)

        if cart.status == 'DELIVERED' or cart.status == 'ORDERED':
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.query_params.get('delete') == 'item':
            if not request.query_params.get('id'):
                return Response({'message': 'id is missing'}, status=status.HTTP_400_BAD_REQUEST)

            item = get_object_or_404(
                models.CartDetails,
                Q(details__placed_by=request.user) &
                Q(id=request.query_params.get('id'))
            )
            item.delete()

            if len(cart.details.all()) == 0:
                cart.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
