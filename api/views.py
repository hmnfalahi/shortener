import requests
from django.db import transaction
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from api.models import Link
from api.serializers import LinkSerializer


class LinkController(RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        response = requests.get('http://127.0.0.1:8000/api/keys/')
        if response.status_code != 200:
            raise Exception(response.content)

        short_url = response.json()['base62']
        serializer.save(short_url=short_url)

