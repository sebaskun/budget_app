# -*- coding: utf-8 -*-
# from decimal import Decimal
# import shelve
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import JsonResponse
# from django.forms.models import model_to_dict

# from braces.views import CsrfExemptMixin
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework import (
    # generics,
    # status,
    viewsets,
)
from rest_framework.decorators import action, detail_route

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# from braces.views import CsrfExemptMixin

from . import serializers

from .models import (
    User,
    GruposVarios,
    Regimen,
    Certificado
)

# from rest_framework.decorators import (
#     api_view,
#     detail_route,
#     list_route,
# )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class GruposVariosViewSet(viewsets.ModelViewSet):
    queryset = GruposVarios.objects.exclude(activo=False)
    serializer_class = serializers.GruposVariosSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('grupo',)


class RegimenViewSet(viewsets.ModelViewSet):
    queryset = Regimen.objects.exclude(activo=False)
    serializer_class = serializers.RegimenSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('categoria_trabajador', 'regimen')

    @action(detail=False)
    def unicos(self, request):
        regimen = Regimen.objects.exclude(activo=False).order_by('regimen__pk').distinct('regimen__pk')
        serializer = serializers.RegimenUnicosSerializer(
            regimen,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @action(detail=True)
    def categorias(self, request, pk=None):
        regimen = Regimen.objects.filter(
            activo=True,
            regimen=pk).order_by("categoria_trabajador__nombre")
        serializer = serializers.RegimenSerializer(
            regimen,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)


class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = Certificado.objects.exclude(activo=False)
    serializer_class = serializers.CertificadoSerializer
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_fields = ('categoria_trabajador', 'regimen')