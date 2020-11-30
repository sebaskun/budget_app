# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

from .api import (
    CategoryEquipmentViewSet,
    # CategoryManpowerViewSet,
    # CategoryMaterialViewSet,
    EquipmentViewSet,
    ManpowerViewSet,
    MaterialViewSet,
    SubcontractViewSet,
    VacunaViewSet,
    # VacunaDeletedViewSet,
    VacunaDetailViewSet,
    # VacunaDetailDeletedViewSet,
    # OverHeadViewSet,
)

router = DefaultRouter()
# router.register(r'category_material', CategoryMaterialViewSet)
router.register(r'category_equipment', CategoryEquipmentViewSet)
# router.register(r'category_manpower', CategoryManpowerViewSet)
router.register(r'manpower', ManpowerViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'material', MaterialViewSet)
router.register(r'subcontract', SubcontractViewSet)
router.register(r'vacuna', VacunaViewSet)
# router.register(r'vacuna_deleted', VacunaDeletedViewSet)
router.register(r'vacuna_detail', VacunaDetailViewSet)
# router.register(r'vacuna_detail_deleted', VacunaDetailDeletedViewSet)
# router.register(r'overhead', OverHeadViewSet)

urlpatterns = [
    url(r'^$', views.ResourceView.as_view(), name="resource"),
    url(r'^api/', include(router.urls)),
    url(r'^manpower$', views.ManpowerResourceView.as_view(), name="manpower_resource"),
    url(r'^material$', views.MaterialResourceView.as_view(), name="material_resource"),
    url(r'^subcontract$', views.SubcontractResourceView.as_view(), name="subcontract_resource"),
    url(r'^equipment$', views.EquipmentResourceView.as_view(), name="equipment_resource"),
    # url(r'^type_manpower$', views.TypeManpowerResourceView.as_view(), name="type_manpower_resource"),
    # url(r'^type_material$', views.TypeMaterialResourceView.as_view(), name="type_material_resource"),
    # url(r'^type_equipment$', views.TypeEquipmentResourceView.as_view(), name="type_equipment_resource"),
]
