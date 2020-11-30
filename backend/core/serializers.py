# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import (
    User,
    GruposVarios,
    Regimen,
    Certificado
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class GruposVariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = GruposVarios
        fields = (
            "id",
            "nombre",
            "grupo",
            "get_grupo_nombre",
            "activo",
            "predeterminado")


class RegimenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Regimen
        fields = (
            "id",
            "regimen",
            "get_regimen_nombre",
            # "tipo",
            # "get_tipo_nombre",
            # "sueldo_manual",
            "sueldo",
            "currency",
            "categoria_trabajador",
            "get_categoria_trabajador_nombre")


class RegimenUnicosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Regimen
        fields = (
            "regimen",
            "get_regimen_nombre")


class CertificadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificado
        fields = "__all__"
