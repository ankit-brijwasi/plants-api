from django.http.request import QueryDict, MultiValueDict
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from nursury import serializers, models


class IsNursury(permissions.BasePermission):
    message = "only nursuries are allowed"

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.type == "nursury"


class NursuryView(APIView):
    '''
    Nursury View

    Allowed Methods: GET, POST, PATCH, DELETE
    '''
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    permission_classes = (permissions.IsAuthenticated, IsNursury)

    def get(self, request, pk=None):
        queryset = models.Plant.objects.all()
        if pk:
            plant = get_object_or_404(queryset, pk=pk)
            serializer = serializers.PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = serializers.PlantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {**request.data}
        data.update({'user': [request.user.id]})

        query_dict = QueryDict('', mutable=True)
        query_dict.update(MultiValueDict(data))

        serializer = serializers.PlantSerializer(data=query_dict)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        plant = get_object_or_404(
            models.Plant,
            Q(pk=pk) &
            Q(user=request.user)
        )
        serializer = serializers.PlantSerializer(
            instance=plant,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        plant = get_object_or_404(
            models.Plant,
            Q(pk=pk) &
            Q(user=request.user)
        )
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
