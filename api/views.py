import requests
from django.db import transaction
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from api.models import Link
from api.serializers import LinkSerializer


# Create your views here.
class LinkController(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                     DestroyModelMixin, GenericAPIView):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #
    #     serializer = self.get_serializer(data=request.data, )
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        response = requests.get('http://127.0.0.1:8000/api/keys/')
        if response.status_code != 200:
            raise Exception(response.content)

        short_url = response.json()['base62']
        serializer.save(short_url=short_url)

    # def get(self, request, *args, **kwargs):
    #     key = Key.objects.create()
    #     serializer = self.serializer_class(instance=key)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

