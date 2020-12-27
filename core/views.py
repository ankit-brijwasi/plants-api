from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializer

from core import models, serializers


class OrderAPIView(APIView):
    def get(self, request):
        orders = get_object_or_404(models.Order, placed_by=request.user)
        serializer = serializers.OrderSerializer(orders, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        data = {**request.data}
        data.update({'placed_by': {'email': request.user.email}})

        serializer = serializers.OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        order = get_object_or_404(models.Order, placed_by=request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
