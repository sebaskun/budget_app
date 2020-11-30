# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import (
    Equipment,
    Manpower,
    Material,
    Subcontract,
    # OverHead,
    CategoryEquipment,
    # CategoryManpower,
    # CategoryMaterial,
    Vacuna,
    VacunaDetail,
)


fields_category = (
    'id',
    'url',
    'name',
    'description',
    "image",
    "get_count"
)

fields_resource = (
    "id",
    "url",
    "code",
    "name",
    "description",
    "unit",
    "currency",
    "cost",
    "pull_in_new_budget",
    # "category",
)


class VacunaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vacuna
        fields = (
            "id",
            "url",
            "nombre",
            "ubicacion",
            "get_ubicacion_display",
            "get_costo_vacuna",
            "moneda",
            "is_deleted"
        )


class VacunaDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = VacunaDetail
        fields = (
            "id",
            "url",
            "vacuna",
            "material",
            "quantity",
            "observacion",
            "get_precio_parcial",
            "get_material_display",
            "get_material_moneda",
            "is_deleted"
        )


# class CategoryManpowerSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = CategoryManpower
#         fields = fields_category


class CategoryEquipmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CategoryEquipment
        fields = fields_category + (
            'padre',
        )


# class CategoryMaterialSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = CategoryMaterial
#         fields = fields_category


class ManpowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manpower
        fields = fields_resource + (
            'sueldo_bruto',
            'type_cost',
            'tipo_regimen',
            'get_type_cost_display',
            'get_tipo_regimen_display',
        )


class MaterialSerializer(serializers.ModelSerializer):
    # category = CategoryMaterialBaseSerializer(many=True, read_only=False)

    class Meta:
        model = Material
        fields = fields_resource + (
            'class_cost', 
            'is_deleted',
        )


class SubcontractSerializer(serializers.ModelSerializer):
    # category = CategoryMaterialBaseSerializer(many=True, read_only=False)

    class Meta:
        model = Subcontract
        fields = fields_resource + (
            'is_deleted',
        )


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = fields_resource + (
            'hours_equipment_operation',
            'potencia',
            'cost',
            'has_combustible',
            'tipo_combustible',
            'category',
            'get_category_display',
            'is_deleted',
        )