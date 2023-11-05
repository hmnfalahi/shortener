from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.models import Link, LinkMember
from api.serializers import LinkSerializer, DRFTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LinkController(RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()
    lookup_field = 'short_url'

    def _ensure_link_member(self, link_id):
        if self.request.user.is_authenticated:
            LinkMember.objects.get_or_create(
                user_id=self.request.user.id,
                link_id=link_id,
            )

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        link, created = Link.objects.get_or_create(url=self.request.data['url'])
        self._ensure_link_member(link_id=link.id)
        serializer = self.serializer_class(instance=link)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get(self, request, *args, **kwargs):
        short_url = kwargs.get('short_url')
        link = Link.objects.filter(short_url=short_url).first()
        self.check_object_permissions(self.request, link)
        link.view_count += 1
        link.save(update_fields=['view_count'])
        return HttpResponseRedirect(redirect_to=link.url)


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer


