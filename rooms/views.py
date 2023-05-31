from django.shortcuts import render
from rest_framework import status, generics, viewsets, mixins
from rest_framework import serializers, permissions
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rooms.models import Room
from rooms.permissions import IsOwner
from rooms.serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):

        max_price = request.GET.get('max_price', None)
        min_price = request.GET.get('min_price', None)
        beds = request.GET.get('beds', None)
        bedrooms = request.GET.get('bedrooms', None)
        bathrooms = request.GET.get('bathrooms', None)
        filter_kwargs = {}
        if max_price is not None:
            filter_kwargs['price__lte'] = max_price
        if min_price is not None:
            filter_kwargs['price__gte'] = min_price
        if beds is not None:
            filter_kwargs['beds__gte'] = beds
        if bedrooms is not None:
            filter_kwargs['bedrooms__gte'] = bedrooms
        if bathrooms is not None:
            filter_kwargs['bathrooms__gte'] = bathrooms

        paginator = self.paginator
        paginator.page_size = 5
        rooms = Room.objects.filter(**filter_kwargs)
        result = paginator.paginate_queryset(rooms, request)
        rooms_serializer = RoomSerializer(result, many=True)
        return paginator.get_paginated_response(rooms_serializer.data)
