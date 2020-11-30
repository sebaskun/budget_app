# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import (
    Client,
)


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            "url",
            "id",
            "name",
            "short_name",
            "initials",
            "ruc",
            "address",
            "logo",
            "get_image_small",
            "get_image_medium",
            "get_image_medium_h",
            "get_image_miniature_50_0",
            "get_image_large"
        ]
