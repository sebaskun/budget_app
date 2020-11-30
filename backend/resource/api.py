# -*- coding: utf-8 -*-
# from decimal import Decimal
# import shelve
# from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http import JsonResponse
# from django.forms.models import model_to_dict

# from braces.views import CsrfExemptMixin
import django_filters.rest_framework
from rest_framework import (
    # generics,
    # status,
    viewsets,
)
# from rest_framework.decorators import detail_route

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# from braces.views import CsrfExemptMixin

from . import serializers

from .models import (
    Manpower,
    Material,
    Equipment,
    Subcontract,
    # OverHead,
    CategoryMaterial,
    CategoryManpower,
    CategoryEquipment,
    Vacuna,
    VacunaDetail,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action


class ManpowerViewSet(viewsets.ModelViewSet):
    queryset = Manpower.objects.all().order_by("name")
    serializer_class = serializers.ManpowerSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        SearchFilter)
    filter_fields = ('code',)
    search_fields = ('code', 'name', 'description')


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.exclude(is_deleted=True).order_by("code")
    serializer_class = serializers.MaterialSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        SearchFilter)
    filter_fields = ('code', 'class_cost')
    search_fields = ('code', 'name', 'description')
    
    @action(detail=True)
    def delete(self, request, pk=None):
        material = self.get_object()
        material.is_deleted = True
        material.save()
        return Response({'status': 'Material eliminado'})


class SubcontractViewSet(viewsets.ModelViewSet):
    queryset = Subcontract.objects.exclude(is_deleted=True).order_by("code")
    serializer_class = serializers.SubcontractSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        SearchFilter)
    filter_fields = ('code',)
    search_fields = ('code', 'name', 'description')
    
    @action(detail=True)
    def delete(self, request, pk=None):
        subcontract = self.get_object()
        subcontract.is_deleted = True
        subcontract.save()
        return Response({'status': 'Subcontrato eliminado'})


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.exclude(is_deleted=True).order_by("code")
    serializer_class = serializers.EquipmentSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        SearchFilter)
    filter_fields = ('code','category',)
    search_fields = ('code', 'name', 'description')

    @action(detail=True)
    def delete(self, request, pk=None):
        equipment = self.get_object()
        equipment.is_deleted = True
        equipment.save()
        return Response({'status': 'Equipo eliminado'})


# class OverHeadViewSet(viewsets.ModelViewSet):
#     queryset = OverHead.objects.all()
#     serializer_class = serializers.OverHeadSerializer
#     filter_backends = (
#         django_filters.rest_framework.DjangoFilterBackend,
#         SearchFilter)
#     filter_fields = ('code',)
#     search_fields = ('code', 'name', 'description')


# class CategoryManpowerViewSet(viewsets.ModelViewSet):
#     queryset = CategoryManpower.objects.all()
#     serializer_class = serializers.CategoryManpowerSerializer
#     filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


# class CategoryMaterialViewSet(viewsets.ModelViewSet):
#     queryset = CategoryMaterial.objects.all()
#     serializer_class = serializers.CategoryMaterialSerializer
#     filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class CategoryEquipmentViewSet(viewsets.ModelViewSet):
    queryset = CategoryEquipment.objects.all()
    serializer_class = serializers.CategoryEquipmentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class VacunaViewSet(viewsets.ModelViewSet):
    queryset = Vacuna.objects.exclude(is_deleted=True)
    serializer_class = serializers.VacunaSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    @action(detail=True)
    def delete(self, request, pk=None):
        vacuna = self.get_object()
        vacuna.is_deleted = True
        vacuna.save()
        return Response({'status': 'Presupuesto de vacuna eliminado'})

# class VacunaDeletedViewSet(viewsets.ModelViewSet):
#     queryset = Vacuna.objects.filter(is_deleted=True)
#     serializer_class = serializers.VacunaSerializer
#     filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class VacunaDetailViewSet(viewsets.ModelViewSet):
    queryset = VacunaDetail.objects.exclude(is_deleted=True)
    serializer_class = serializers.VacunaDetailSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    @action(detail=True)
    def delete(self, request, pk=None):
        vacuna = self.get_object()
        vacuna.is_deleted = True
        vacuna.save()
        return Response({'status': 'Vacuna eliminado'})


# class VacunaDetailDeletedViewSet(viewsets.ModelViewSet):
#     queryset = VacunaDetail.objects.filter(is_deleted=True)
#     serializer_class = serializers.VacunaDetailSerializer
#     filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)