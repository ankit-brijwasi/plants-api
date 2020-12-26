from django.http.request import QueryDict, MultiValueDict
from django.shortcuts import get_object_or_404

from rest_framework import parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from nursury import serializers, models

class NursuryView(APIView):
    '''
    Nursury View
    ALLOWED METHODS = GET, POST
    '''
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)

    def get(self, request, pk=None):
        queryset = models.Plant.objects.all()
        if pk:
            plant = get_object_or_404(queryset, pk=pk)
            serializer = serializers.PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = serializers.PlantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.type == "nursury":
            data = { **request.data }
            data.update({ 'user': [request.user.id] })
            
            query_dict = QueryDict('', mutable=True)
            query_dict.update(MultiValueDict(data))

            serializer = serializers.PlantSerializer(data=query_dict)        
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Access is forbidden'}, status=status.HTTP_403_FORBIDDEN)