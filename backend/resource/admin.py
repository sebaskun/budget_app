# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.contrib import admin
# from reversion.admin import VersionAdmin
# # from tabbed_admin import TabbedModelAdmin
# from . import models


# @admin.register(models.Manpower)
# class ManPowerAdmin(VersionAdmin):
#     search_fields = ['nombre']
#     list_filter = ('type_manpower', 'moneda')
#     list_display = [
#         'nombre',
#         'unidad',
#         'type_manpower',
#         'moneda',
#         'precio'
#     ]

#     # tab_overview = (
#     #     (None, {
#     #         'fields': ('nombre', 'unidad', 'type_manpower')
#     #     }),
#     # )

#     # tab_cost = (
#     #     ('Costo', {
#     #         'fields': ('type_cost', 'moneda', 'precio')
#     #     }),
#     # )
#     # tabs = [
#     #     ('Overview', tab_overview),
#     #     ('Costos', tab_cost)
#     # ]


# @admin.register(models.Material)
# class MaterialAdmin(VersionAdmin):
#     search_fields = ['nombre']
#     list_filter = ('type_material', 'moneda')
#     list_display = [
#         'nombre',
#         'unidad',
#         'type_material',
#         'moneda',
#         'precio'
#     ]


# @admin.register(models.Equipment)
# class EquipmentAdmin(VersionAdmin):
#     search_fields = ['nombre']
#     list_filter = ('type_equipment', 'moneda')
#     list_display = [
#         'nombre',
#         'unidad',
#         'type_equipment',
#         'moneda',
#         'precio'
#     ]


# @admin.register(models.TypeManpower)
# class TypeManpowerAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.TypeMaterial)
# class TypeMaterialAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.TypeEquipment)
# class TypeEquipmentAdmin(admin.ModelAdmin):
#     pass