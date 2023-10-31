from rest_framework import serializers

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
