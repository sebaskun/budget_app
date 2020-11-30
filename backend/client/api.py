# -*- coding: utf-8 -*-

from rest_framework import (
    viewsets,
)
# from rest_framework.decorators import detail_route

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# from braces.views import CsrfExemptMixin

# from rest_framework_extensions.mixins import NestedViewSetMixin


from . import serializers

from .models import (
    Client,
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('name')
    serializer_class = serializers.ClientSerializer
