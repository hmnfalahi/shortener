from rest_framework import serializers
from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from api.models import Link


class LinkSerializer(serializers.ModelSerializer):
    # shortUrl = serializers.CharField(source='short_url')
    # viewCount = serializers.CharField(source='view_count')

    class Meta:
        fields = '__all__'
        model = Link
        extra_kwargs = {
            'shortUrl': {'required': False, 'read_only': True},
            'viewCount': {'required': False, 'read_only': True},
        }

        # read_only_fields = ['short_url', 'view_count']


class DRFTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['email'] = user.email
        return token


