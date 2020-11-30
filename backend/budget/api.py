# -*- coding: utf-8 -*-
# from decimal import Decimal
# import shelve
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Count

from django_filters import rest_framework as filters
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Max
from decimal import Decimal

from rest_framework import (
    generics,
    # status,
    viewsets,
    serializers as ser
)
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import (
    api_view,
    detail_route,
    list_route,
)
from rest_framework.decorators import action

from rest_framework.views import APIView
# from braces.views import CsrfExemptMixin

from . import serializers
from .views import copy_task

from .models import (
    # OverHeadBudget,
    Budget,
    Equipment,
    EquipmentBudget,
    EquipmentTask,
    Manpower,
    ManpowerBudget,
    ManpowerTask,
    Material,
    MaterialBudget,
    MaterialTask,
    STATUS_BUDGET,
    Subcontract,
    SubcontractBudget,
    SubcontractTask,
    TaskBudget,
    EPPBudget,
    EPPBudgetDetail,
    CertificacionBudget,
)


def get_overhead_manpower(budget_id, show_items=True):
    rows = []
    manpowers = ManpowerBudget.objects.filter(budget_id=budget_id, type_cost="I").order_by("manpower__name")
    fields = (
        "pk", "get_resource_label", "quantity", "time_valorize",
        "get_business_cost", "get_overhead_cost"
    )
    for item in manpowers:
        row = {}
        for field in fields:
            row[field] = getattr(item, field)
        rows.append(row)
    total = Decimal("0.00")
    hydration = Decimal("0.00")
    epp = Decimal("0.00")
    for x in rows:
        total += Decimal(x['get_overhead_cost'])

    if show_items:
        return {
            "total": total,
            "items": rows
        }
    return {"total": total}


def get_close_direct(budget_id, show_items=True):
    rows = []
    manpowers = ManpowerTask.objects.filter(task__budget_id=budget_id).order_by("pk")
    sum_manpowers = 0
    for item in manpowers:
        sum_manpowers += round(item.get_subtotal * item.task.quantity, 2)

    equipments = EquipmentTask.objects.filter(task__budget_id=budget_id).order_by("pk")
    sum_equipments = 0
    for item in equipments:
        sum_equipments += round(item.get_subtotal * item.task.quantity, 2)

    materials = MaterialTask.objects.filter(
        task__budget_id=budget_id, material_budget__is_subcontract=False).order_by("pk")
    sum_materials = 0
    for item in materials:
        sum_materials += round(item.get_subtotal * item.task.quantity, 2)

    subcontracts = SubcontractTask.objects.filter(
        task__budget_id=budget_id).order_by("pk")
    sum_subcontracts = 0
    for item in subcontracts:
        sum_subcontracts += round(item.get_subtotal * item.task.quantity, 2)

    min_tools = ManpowerTask.objects.filter(task__budget_id=budget_id).order_by("pk")
    sum_min_tools = 0
    for item in manpowers:
        sum_min_tools += round(item.get_subtotal * item.task.percentage_minor_tools * item.task.quantity, 2)

    rows = {
        "manpowers": sum_manpowers,
        "equipments": sum_equipments,
        "materials": sum_materials,
        "subcontracts": sum_subcontracts,
        "min_tools": sum_min_tools,
    }

    total = sum_manpowers + sum_equipments + sum_materials + sum_subcontracts + sum_min_tools
    if show_items:
        return {
            "total": total,
            "items": rows
        }
    return {"total": total}


def get_standby_manpower(budget_id, show_items=True):
    rows = []
    manpowers = ManpowerBudget.objects.filter(budget_id=budget_id, type_cost="D").order_by("manpower__name")
    fields = (
        "pk", "get_resource_label", "quantity", "time_valorize", "get_standby_estimated_hours",
        "get_standby_hours", "get_cost_unit", "get_standby_cost", "get_standby_hydration",
        "get_standby_epp"
    )
    for item in manpowers:
        row = {}
        for field in fields:
            row[field] = getattr(item, field)
        rows.append(row)
    total = Decimal("0.00")
    hydration = Decimal("0.00")
    epp = Decimal("0.00")
    for x in rows:
        total += Decimal(x['get_standby_cost'])
        hydration += Decimal(x['get_standby_hydration'])
        epp += Decimal(x['get_standby_epp'])

    print("get_standby_manpower::", total, hydration, epp, rows)
    if show_items:
        return {
            "total": total,
            "hydration": hydration,
            "epp": epp,
            "items": rows
        }
    return {"total": total}


def get_overhead_material(budget_id, show_items=True, type_material="S"):
    rows = []
    material = MaterialBudget.objects.filter(budget_id=budget_id, type_material=type_material).order_by("material__name")
    fields = (
        "pk", "get_resource_label", "quantity", "time_valorize", "amortization", "get_cost_unit", "get_overhead_cost"
    )
    for item in material:
        row = {}
        for field in fields:
            row[field] = getattr(item, field)
        rows.append(row)
    total = Decimal("0.00")
    for x in rows:
        total += Decimal(x['get_overhead_cost'])
    if show_items:
        return {
            "total": total,
            "items": rows
        }
    return {"total": total}


def get_standby_equipment(budget_id, show_items=True):
    rows = []
    equipments = EquipmentBudget.objects.filter(budget_id=budget_id).order_by("equipment__name")
    for item in equipments:
        row = {
            "pk": item.pk,
            "get_resource_label": item.get_resource_label,
            "quantity": item.quantity,
            "time_valorize": item.time_valorize,
            "get_standby_estimated_hours": item.get_standby_estimated_hours,
            "get_standby_hours": item.get_standby_hours,
            "get_cost_unit": item.get_cost_unit,
            "get_standby_cost": item.get_standby_cost,
            "hours_equipment_operation": item.hours_equipment_operation
        }
        rows.append(row)
    total = Decimal("0.00")
    for x in rows:
        total += Decimal(x['get_standby_cost'])
    if show_items:
        return {
            "total": total,
            "items": rows
        }
    return {"total": total}


# def calculatePrice(user, modified):
#     print("Llamada a calculate: ", user, modified.task.budget)


class ManpowerTaskViewSet(viewsets.ModelViewSet):
    queryset = ManpowerTask.objects.all()
    serializer_class = serializers.ManpowerTaskSerializer

    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     calculatePrice(user=self.request.user, modified=instance)


class MaterialTaskViewSet(viewsets.ModelViewSet):
    queryset = MaterialTask.objects.all()
    serializer_class = serializers.MaterialTaskSerializer


class SubcontractTaskViewSet(viewsets.ModelViewSet):
    queryset = SubcontractTask.objects.all()
    serializer_class = serializers.SubcontractTaskSerializer


class EquipmentTaskViewSet(viewsets.ModelViewSet):
    queryset = EquipmentTask.objects.all()
    serializer_class = serializers.EquipmentTaskSerializer


class CreateListTaskMixin:
    """Allows bulk creation of tasks."""
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)


class TaskBudgetViewSet(viewsets.ModelViewSet):
    # authentication_classes = []

    queryset = TaskBudget.objects.all().order_by("position")
    serializer_class = serializers.TaskBudgetSerializer

    # def get_queryset(self):
    #     budget = self.kwargs['budget']
    #     return TaskBudget.objects.filter(budget=budget)

    @detail_route()
    def manpowers(self, request, pk=None):
        task = self.get_object()
        serializer = serializers.ManpowerTaskSerializer(
            task.tasks_manpower_task.all(),
            context={'request': request}, many=True)
        return Response(serializer.data)

    @detail_route()
    def materials(self, request, pk=None):
        task = self.get_object()
        serializer = serializers.MaterialTaskSerializer(
            task.tasks_material_task.all(),
            context={'request': request}, many=True)
        return Response(serializer.data)

    @detail_route()
    def subcontracts(self, request, pk=None):
        task = self.get_object()
        serializer = serializers.SubcontractTaskSerializer(
            task.tasks_subcontract_task.all(),
            context={'request': request}, many=True)
        return Response(serializer.data)

    @detail_route()
    def equipments(self, request, pk=None):
        task = self.get_object()
        serializer = serializers.EquipmentTaskSerializer(
            task.tasks_equipment_task.all(),
            context={'request': request}, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def copy(self, request, pk=None):
        task = self.get_object()
        new_task = copy_task(task)
        serializer = serializers.TaskBudgetSerializer(
            new_task,
            context={'request': request}
        )
        return Response(serializer.data)

    # @method_decorator(csrf_exempt)
    # def dispatch(self, *args, **kwargs):
    #     return super(TaskBudgetViewSet, self).dispatch(*args, **kwargs)


@api_view(['GET'])
def delete_all_tasks(request, pk=None):
    if (pk is not None):
        budget = Budget.objects.get(pk=pk)
        task_deleted = budget.tasks_budget.all().delete()
        return Response({"message": task_deleted})
    return Response({"message": "No se ha seleccionado un PK de Budget"})


class BudgetTreeViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.exclude(is_deleted=True)
    serializer_class = serializers.BudgetTreeSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status', 'is_archived', 'client')
    search_fields = ('title', 'code')


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.exclude(is_deleted=True)
    serializer_class = serializers.BudgetSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status', 'is_archived', 'client')
    search_fields = ('title', 'code')

    @detail_route()
    def tree(self, request, pk=None):
        budget = self.get_object()
        # serializer = serializers.BudgetTreeSerializer(
        #     budget.tree,
        #     context={'request': request},
        #     many=True
        # )
        return Response(budget.tree)

    @detail_route()
    def tasks(self, request, pk=None):
        budget = self.get_object()
        # task_list = [task for task in budget.tasks_budget.all() if task.get_outline_level == 1]
        task_list = budget.tasks_budget.all()
        serializer = serializers.TaskBudgetSerializer(
            # budget.tasks_budget.all(),
            task_list,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @detail_route()
    def manpowers(self, request, pk=None):
        budget = self.get_object()
        serializer = serializers.ManpowerBudgetSerializer(
            budget.manpowers_budget.all().order_by("manpower__name"),
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @detail_route()
    def materials(self, request, pk=None):
        budget = self.get_object()
        materials = budget.materials_budget.exclude(is_deleted=True).order_by("material__name")
        type_material = request.query_params.get('type_material')
        if type_material:
            materials = materials.filter(type_material=type_material)
        serializer = serializers.MaterialBudgetSerializer(
            materials,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @detail_route()
    def subcontracts(self, request, pk=None):
        budget = self.get_object()
        subcontracts = budget.subcontracts_budget.exclude(is_deleted=True).order_by("subcontract__name")
        serializer = serializers.SubcontractBudgetSerializer(
            subcontracts,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @detail_route()
    def equipments(self, request, pk=None):
        budget = self.get_object()
        equipments = budget.equipments_budget.exclude(is_deleted=True).order_by("equipment__name") 
        category_equipment = request.query_params.get('category')
        if category_equipment:
            equipments = equipments.filter(category=category_equipment)        
        serializer = serializers.EquipmentBudgetSerializer(
            equipments,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @detail_route()
    def epps(self, request, pk=None):
        budget = self.get_object()
        serializer = serializers.EPPBudgetSerializer(
            budget.epps_budget.exclude(is_deleted=True),
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @action(detail=True)
    def delete(self, request, pk=None):
        budget = self.get_object()
        budget.is_deleted = True
        budget.save()
        return Response({'status': 'Presupuesto eliminado'})

    # @action(methods=['get'], detail=True)
    # def copy(self, request, pk=None):
    #     budget = self.get_object()
    #     budget2 = budget.clone(attrs={"title":"copia-{0}".format(budget.title)})
    #     serializer = serializers.BudgetSerializer(
    #         budget2,
    #         context={'request': request}
    #     )
    #     return Response(serializer.data)


class ManpowerBudgetViewSet(viewsets.ModelViewSet):
    queryset = ManpowerBudget.objects.all().order_by("manpower__name")
    serializer_class = serializers.ManpowerBudgetSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('budget', 'manpower')


class MaterialBudgetViewSet(viewsets.ModelViewSet):
    queryset = MaterialBudget.objects.all().order_by("material__name")
    serializer_class = serializers.MaterialBudgetSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('budget', 'material','type_material')

    @action(detail=True)
    def delete(self, request, pk=None):
        material = self.get_object()
        material.is_deleted = True
        material.save()
        return Response({'status': 'Material eliminado'})


class SubcontractBudgetViewSet(viewsets.ModelViewSet):
    queryset = SubcontractBudget.objects.all().order_by("subcontract__name")
    serializer_class = serializers.SubcontractBudgetSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('budget', 'subcontract')

    @action(detail=True)
    def delete(self, request, pk=None):
        subcontrato = self.get_object()
        subcontrato.is_deleted = True
        subcontrato.save()
        return Response({'status': 'Subcontrato eliminado'})

class EquipmentBudgetViewSet(viewsets.ModelViewSet):
    queryset = EquipmentBudget.objects.all().order_by("equipment__name")
    serializer_class = serializers.EquipmentBudgetSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('budget', 'equipment','category')

    @action(detail=True)
    def delete(self, request, pk=None):
        equipo = self.get_object()
        equipo.is_deleted = True
        equipo.save()
        return Response({'status': 'Equipo eliminado'})


# class OverHeadBudgetViewSet(viewsets.ModelViewSet):
#     """
#     Clase que mostrará todos los items de Gastos Generales de un presupuesto
#     """
#     queryset = OverHeadBudget.objects.all().order_by("overhead__name")
#     serializer_class = serializers.OverHeadBudgetSerializer

#     filter_backends = (DjangoFilterBackend,)
#     filter_fields = ('budget', 'overhead')


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SubTotalManpowerTaskBudgetView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        task_id = kwargs.get('task_id', None)
        sql = """
        select c.currency, b.quantity, (c.price * b.efficiency * b.quantity) as sub_total_manpower
        from
            budget_taskbudget a inner join budget_manpowertask b on a.id=b.task_id
            inner join budget_manpowerbudget c on b.manpower_id=c.manpower_id
        where a.budget_id=%s and b.task_id=%s and c.budget_id=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [budget_id, task_id, budget_id])
            rows = dictfetchall(cursor)
        total_price = 0
        total_quantity = 0
        for x in rows:
            total_price += x['sub_total_manpower']
            total_quantity += x['quantity']
        result = {
            "total_price": total_price,
            "total_quantity": total_quantity,
            "items": rows
        }
        return Response(result)


class SubTotalMaterialTaskBudgetView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        task_id = kwargs.get('task_id', None)
        sql = """
        select c.currency, (c.price * b.efficiency * b.quantity) as sub_total_material
        from
            budget_taskbudget a inner join budget_materialtask b on a.id=b.task_id
            inner join budget_materialbudget c on b.material_id=c.material_id
        where a.budget_id=%s and b.task_id=%s and c.budget_id=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [budget_id, task_id, budget_id])
            rows = dictfetchall(cursor)
        total = 0
        for x in rows:
            total += x['sub_total_material']
        result = {
            "total": total,
            "items": rows
        }
        return Response(result)


class SubTotalEquipmentTaskBudgetView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        task_id = kwargs.get('task_id', None)
        sql = """
        select c.currency, (c.price * b.efficiency * b.quantity) as sub_total_equipment
        from
            budget_taskbudget a inner join budget_equipmenttask b on a.id=b.task_id
            inner join budget_equipmentbudget c on b.equipment_id=c.equipment_id
        where a.budget_id=%s and b.task_id=%s and c.budget_id=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [budget_id, task_id, budget_id])
            rows = dictfetchall(cursor)
        total = 0
        for x in rows:
            total += x['sub_total_equipment']
        result = {
            "total": total,
            "items": rows
        }
        return Response(result)


class ManpowerOverheadBudgetView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        return Response(get_overhead_manpower(budget_id))


class StandbyOverheadBudgetView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)

        return Response(get_overhead_manpower(budget_id))


class CloseDirectView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)

        return Response(get_close_direct(budget_id))


# class MaterialOverheadBudgetView(APIView):

#     parser_classes = (JSONParser,)

#     def get(self, request, format=None, *args, **kwargs):
#         budget_id = kwargs.get('badget_id', None)
#         type_material = kwargs.get('type_material', None)
#         sql = """
#         SELECT a.*, b.name
#             FROM budget_materialbudget a inner join resource_material b on a.material_id = b.id
#             where a.budget_id = %s and a.type_material = %s
#             order by b.name;
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(sql, [budget_id, type_material])
#             rows = dictfetchall(cursor)
#         return Response(rows)


class BudgetOverheadMaterialView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        type_material = kwargs.get('type_material', None)
        # print("*-*-*-*")
        x = get_overhead_material(budget_id, True, type_material)
        # print("Mi JSON", x)
        return Response(x)


class ManpowerSummaryBudgetView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        return Response(get_standby_manpower(budget_id))


class EquipmentSummaryBudgetView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        return Response(get_standby_equipment(budget_id))


class BudgetOverheadStandbyView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        result = {
            "equipment": get_standby_equipment(budget_id, False)['total'],
            "manpower": get_standby_manpower(budget_id, False)['total']
        }
        return Response(result)


class BudgetStandbyEquipmentView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        return Response(get_standby_equipment(budget_id))


class BudgetStandbyManpowerView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        budget_id = kwargs.get('badget_id', None)
        return Response(get_standby_manpower(budget_id))


class StatusBudgetView(APIView):
    # queryset = Budget.objects.all()
    # serializer_class = serializers.StatusBudgetSerializer
    # get_status2 = ser.SerializerMethodField()

    # def get_queryset(self):
    #     qs = Budget.objects.values(
    #         'status').annotate(
    #         budget_count=Count('status'))
    #     return qs
    parser_classes = (JSONParser,)

    def get(self, request, format=None):

        status_list = []
        for status in STATUS_BUDGET:
            item = {
                "code": status[0],
                "name": status[1],
                "get_count": Budget.objects.filter(status=status[0]).count()
            }
            status_list.append(item)
        return Response(status_list)


class ChildrenTaskBudgetView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, format=None, *args, **kwargs):
        task_id = kwargs.get('task_id', None)
        child_list = []
        if task_id:
            task = get_object_or_404(TaskBudget, id=task_id)
            children = task.get_children
            for child in children:
                item = {
                    "id": child.id,
                    "name": child.name,
                }
                child_list.append(item)
        return Response(child_list)


@api_view(['GET'])
def get_children_task(request, pk=None):
    if (pk is not None):
        child_list = []
        task = get_object_or_404(TaskBudget, pk=pk)
        children = task.get_children
        for child in children:
            item = {
                "id": child.id,
                "name": child.name,
            }
            child_list.append(item)
        return Response(child_list)
    return Response({"message": "No se ha seleccionado un PK de Task"})

@api_view(['post','get'])
def nodeapi(request):
    if request.data['method']=="insert":
        budgetid = request.data.get('budgetid', None)
        if not budgetid:
            return
        if request.data.get('taskid', None):
        # if hasattr(request.data, 'taskid'):
        # father, is_new = TaskBudget.objects.get_or_create(pk=request.data['taskid'])
            father = get_object_or_404(TaskBudget, pk=request.data['taskid'])
            uid = father.budget.tasks_budget.all().aggregate(Max('uid'))
            uid = uid['uid__max']+1
            task = TaskBudget(
                budget=father.budget,
                wbs=father.wbs+'.1', ###
                outline_level=father.outline_level +1,
                name="Nueva Tarea",
                unit=father.unit,
                efficiency=father.efficiency,
                quantity= father.quantity,
                projected_start_date=father.projected_start_date,
                projected_finish_date=father.projected_finish_date,
                # moneda=father.moneda,
                # price=father.price,
                position=father.position+1, ###
                uid=uid, ###
                percentage_minor_tools = father.percentage_minor_tools,
                # apu_material_cost = father.apu_material_cost,
                # apu_equipment_cost = father.apu_equipment_cost,
                # apu_manpower_cost = father.apu_manpower_cost
            )
        else:
            uid = 0
            budget = Budget.objects.get(pk=budgetid)
            task = TaskBudget(budget_id=budgetid, uid=uid, name=budget.title)
        task.save()
        task.budget.fix_tasks()
    if request.data['method']=="delete":
        task = get_object_or_404(TaskBudget, pk=request.data['taskid'])
        task.delete()
        task.budget.fix_tasks()
    if request.data['method']=="+level":
        task = get_object_or_404(TaskBudget, pk=request.data['taskid'])
        task.outline_level = task.outline_level + 1
        task.save()
        task.budget.fix_tasks()
    if request.data['method']=="-level":
        task = get_object_or_404(TaskBudget, pk=request.data['taskid'])
        task.outline_level = task.outline_level - 1
        task.save()
        task.budget.fix_tasks()
    if request.data['method']=="+position":
        task = get_object_or_404(TaskBudget, pk=request.data['taskid'])
        task.position = task.position + 2
        task.save()
        task.budget.fix_tasks()
    if request.data['method']=="-position":
        task = get_object_or_404(TaskBudget, pk=request.data['taskid'])
        task.position = task.position - 2
        task.save()
        task.budget.fix_tasks()

    return Response(request.data)


class EPPBudgetViewSet(viewsets.ModelViewSet):
    queryset = EPPBudget.objects.exclude(is_deleted=True)
    serializer_class = serializers.EPPBudgetSerializer
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_fields = ('categoria_trabajador', 'regimen')


class EPPBudgetDeletedViewSet(viewsets.ModelViewSet):
    queryset = EPPBudget.objects.filter(is_deleted=True)
    serializer_class = serializers.EPPBudgetSerializer
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_fields = ('categoria_trabajador', 'regimen')


class EPPBudgetDetailViewSet(viewsets.ModelViewSet):
    queryset = EPPBudgetDetail.objects.all()
    serializer_class = serializers.EPPBudgetDetailSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_fields = ('epp_budget',)
    # search_fields = ('id','epp_budget')
    


class CertificacionBudgetViewSet(viewsets.ModelViewSet):
    queryset = CertificacionBudget.objects.exclude(is_deleted=True)
    serializer_class = serializers.CertificacionBudgetSerializer
    filter_fields = ('budget',)
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_fields = ('categoria_trabajador', 'regimen')

class CertificacionBudgetDeletedViewSet(viewsets.ModelViewSet):
    queryset = CertificacionBudget.objects.filter(is_deleted=True)
    serializer_class = serializers.CertificacionBudgetSerializer
