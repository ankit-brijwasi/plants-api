from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from nursury.serializers import Plant, PlantSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from core.models import Order, OrderDetails

User = get_user_model()


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['plant'] = PlantSerializer(
            Plant.objects.get(pk=data['plant'])
        ).data
        return data


class OrderSerializer(serializers.ModelSerializer):
    placed_by = UserSerializer(read_only=False)
    details = OrderDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop('placed_by')
        user = User.objects.get(email=user.get('email'))

        order, _ = Order.objects.get_or_create(placed_by=user)

        order_details = validated_data.pop('details')
        for order_detail in order_details:
            temp, created = order.details.get_or_create(
                plant=order_detail.get('plant'))
            temp.quantity = order_detail.get('quantity')
            temp.save()

        return order
