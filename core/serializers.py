from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from nursury.serializers import Plant, PlantSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from core.models import Cart, CartDetails

User = get_user_model()


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetails
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['plant'] = PlantSerializer(
            Plant.objects.get(pk=data['plant'])
        ).data
        return data


class CartSerializer(serializers.ModelSerializer):
    placed_by = UserSerializer(read_only=False)
    details = CartDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Cart
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop('placed_by')
        user = User.objects.get(email=user.get('email'))

        cart, _ = Cart.objects.get_or_create(placed_by=user, status='CART')

        cart_details = validated_data.pop('details')
        for cart_detail in cart_details:
            temp, created = cart.details.get_or_create(
                plant=cart_detail.get('plant'))
            temp.quantity = cart_detail.get('quantity')
            temp.save()

        return cart
