# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.urls import path, re_path

from rest_framework.routers import DefaultRouter

from . import views
from .api import (
    BudgetOverheadMaterialView,
    BudgetOverheadStandbyView,
    BudgetStandbyEquipmentView,
    BudgetStandbyManpowerView,
    BudgetViewSet,
    CloseDirectView,
    EquipmentBudgetViewSet,
    EquipmentSummaryBudgetView,
    EquipmentTaskViewSet,
    ManpowerBudgetViewSet,
    ManpowerOverheadBudgetView,
    ManpowerSummaryBudgetView,
    ManpowerTaskViewSet,
    MaterialBudgetViewSet,
    # MaterialOverheadBudgetView,
    MaterialTaskViewSet,
    StatusBudgetView,
    SubTotalEquipmentTaskBudgetView,
    SubTotalManpowerTaskBudgetView,
    SubTotalMaterialTaskBudgetView,
    SubcontractBudgetViewSet,
    SubcontractTaskViewSet,
    TaskBudgetViewSet,
    delete_all_tasks,
    get_children_task,
    nodeapi,
    EPPBudgetViewSet,
    EPPBudgetDeletedViewSet,
    EPPBudgetDetailViewSet,
    # EPPBudgetDetailDeletedViewSet,
    CertificacionBudgetViewSet,
    CertificacionBudgetDeletedViewSet,
    BudgetTreeViewSet
)

app_name = "budget"

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet)
# router.register(r'budget_tree', BudgetTreeViewSet)
router.register(r'tasks', TaskBudgetViewSet)
router.register(r'manpower_budget', ManpowerBudgetViewSet)
router.register(r'material_budget', MaterialBudgetViewSet)
router.register(r'subcontract_budget', SubcontractBudgetViewSet)
router.register(r'equipment_budget', EquipmentBudgetViewSet)
# router.register(r'overhead_budget', OverHeadBudgetViewSet)
router.register(r'manpower_task', ManpowerTaskViewSet)
router.register(r'material_task', MaterialTaskViewSet)
router.register(r'subcontract_task', SubcontractTaskViewSet)
router.register(r'equipment_task', EquipmentTaskViewSet)
router.register(r'epp_budget', EPPBudgetViewSet)
# router.register(r'epp_budget_deleted', EPPBudgetDeletedViewSet)
router.register(r'epp_budget_detail', EPPBudgetDetailViewSet)
# router.register(r'epp_budget_detail_deleted', EPPBudgetDetailDeletedViewSet)
router.register(r'certificacion_budget', CertificacionBudgetViewSet)
# router.register(r'certificacion_budget_deleted', CertificacionBudgetDeletedViewSet)

urlpatterns = [
    re_path(r'^$', views.BudgetView.as_view(), name="budget_view"),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/status/$', StatusBudgetView.as_view(), name="status_budget"),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/manpower/summary$',
        ManpowerSummaryBudgetView.as_view(),
        name='budget_manpower_summary'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/equipment/summary$',
        EquipmentSummaryBudgetView.as_view(),
        name='budget_equipment_summary'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/manpowers/(?P<task_id>\w+)/apu$',
        SubTotalManpowerTaskBudgetView.as_view(),
        name='budgets_manpowers_apu'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/materials/(?P<task_id>\w+)/apu$',
        SubTotalMaterialTaskBudgetView.as_view(),
        name='budgets_materials_apu'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/equipments/(?P<task_id>\w+)/apu$',
        SubTotalEquipmentTaskBudgetView.as_view(),
        name='budgets_equipments_apu'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/manpower/overhead$',
        ManpowerOverheadBudgetView.as_view(),
        name='budget_manpower_overhead'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/direct/close$',
        CloseDirectView.as_view(),
        name='budget_direct_close'),
    re_path(
        r'^api/budgets/(?P<pk>\w+)/tasks/delete$',
        delete_all_tasks,
        name='budget_tasks_delete'),
    re_path(
        r'^api/tasks/(?P<pk>\w+)/children$',
        get_children_task,
        name='get_children_task'),
    re_path(
        r'^api/nodeapi$',
        nodeapi,
        name='nodeapi'),
    re_path(
        r'^(?P<pk>\w+)/download$',
        views.export_budget_xml,
        name='budget_download'),

    # Inicio: Standby
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/manpower/standby$',
        BudgetStandbyManpowerView.as_view(),
        name='budget_standby_manpower'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/equipment/standby$',
        BudgetStandbyEquipmentView.as_view(),
        name='budget_standby_equipment'),
    # Fin: Standby

    # Inicio: Overhead
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/standby/overhead$',
        BudgetOverheadStandbyView.as_view(),
        name='budget_overhead_standby'),
    re_path(
        r'^api/budgets/(?P<badget_id>\w+)/material/(?P<type_material>\w+)/overhead$',
        BudgetOverheadMaterialView.as_view(),
        name='budget_overhead_material'),
    # Fin: Overhead
]
