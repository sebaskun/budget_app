# -*- coding: utf-8 -*-
from decimal import Decimal
from rest_framework import serializers

from .models import (
    Budget,
    ManpowerBudget,
    MaterialBudget,
    SubcontractBudget,
    EquipmentBudget,
    # OverHeadBudget,
    ManpowerTask,
    MaterialTask,
    SubcontractTask,
    EquipmentTask,
    TaskBudget,
    EPPBudget,
    EPPBudgetDetail,
    CertificacionBudget,
)

from ..client.models import Client
from ..client.serializers import ClientSerializer
from datetime import datetime


class CertificacionBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:certificacionbudget-detail",
    )

    class Meta:
        model = CertificacionBudget
        fields = (
            "id",
            "url",
            "budget",
            "certificado",
            "moneda",
            "importe",
            "get_certificado_display",
            "is_deleted",
        )


class EPPBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:eppbudget-detail",
    )

    class Meta:
        model = EPPBudget
        fields = (
            "id",
            "url",
            "budget",
            "tipo_epp",
            "get_tipo_epp_display",
            "get_costo",
            "get_costo_mes",
            "is_deleted",
        )


class EPPBudgetDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:eppbudgetdetail-detail",
    )

    class Meta:
        model = EPPBudgetDetail
        fields = (
            "id",
            "url",
            "epp_budget",
            "material",
            "unidad",
            "periodo_reposicion",
            "quantity",
            "get_demanda",
            "get_parcial",
            "get_material_display",
            "is_deleted",
        )


class ManpowerTaskSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:manpowertask-detail",
    )

    class Meta:
        model = ManpowerTask
        fields = (
            'id',
            'url',
            'task',
            'get_task_name',
            'get_manpower_name',
            'manpower',
            'quantity',
            'manpower_budget',
            'get_efficiency',
            # 'get_price_manpower',
            'get_subtotal',
            'get_resource_label',
            'get_resource_price'
        )


class MaterialTaskSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:materialtask-detail",
    )

    class Meta:
        model = MaterialTask
        fields = (
            'id',
            'url',
            'task',
            'get_task_name',
            'material',
            'quantity',
            'material_budget',
            'efficiency',
            'get_efficiency',
            # 'price',
            'get_subtotal',
            'get_resource_label',
            'get_resource_price'
        )


class SubcontractTaskSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:subcontracttask-detail",
    )

    class Meta:
        model = SubcontractTask
        fields = (
            'id',
            'url',
            'task',
            'get_task_name',
            'subcontract',
            'quantity',
            'subcontract_budget',
            'efficiency',
            'get_efficiency',
            # 'price',
            'get_subtotal',
            'get_resource_label',
            'get_resource_price'
        )


class EquipmentTaskSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:equipmenttask-detail",
    )

    class Meta:
        model = EquipmentTask
        fields = (
            'id',
            'url',
            'task',
            'get_task_name',
            'equipment',
            'quantity',
            'equipment_budget',
            'get_efficiency',
            # 'price',
            'get_subtotal',
            'get_resource_label',
            'get_resource_price'
        )


class TaskBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:taskbudget-detail",
    )
    # manpowers = serializers.HyperlinkedIdentityField(
    #     view_name='budget:taskbudget-manpowers'
    # )

    class Meta:
        model = TaskBudget
        fields = (
            "url",
            "id",
            "budget",
            "wbs",
            "name",
            "unit",
            "efficiency",
            "efficiency_divider",
            "get_efficiency",
            "quantity",
            "percentage_minor_tools",
            "projected_start_date",
            "projected_finish_date",
            "uid",
            "position",
            "outline_level",
            "get_subtotal_manpower",
            "get_subtotal_material",
            "get_subtotal_equipment",
            "get_subtotal_subcontract",
            "get_subtotal_minor_tools",
            "get_unit_subtotal",
            "get_subtotal",
            "data",
            "text"
        )

    # def get_fields(self):
    #     fields = super(TaskBudgetSerializer, self).get_fields()
    #     fields["get_children"] = TaskBudgetSerializer(many=True, read_only=True)
    #     fields["get_children"].required = False
    #     return fields


class BudgetTreeSerializer(serializers.ModelSerializer):
    """
    Se preparó esta clase para mostrar el arbol de partidas y actividades
    """

    class Meta:
        model = Budget
        fields = (
            "id",
            "tree"
        )


class BudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:budget-detail",
    )

    code = serializers.CharField(read_only=True)

    # tasks_listing = serializers.HyperlinkedIdentityField(
    #     view_name='budget:budget-tasks',
    # )
    # manpowers_listing = serializers.HyperlinkedIdentityField(
    #     view_name='budget:budget-manpowers',
    # )
    # client = serializers.IntegerField()

    class Meta:
        model = Budget
        fields = (
            "id",
            "url",
            "code",
            "title",
            "location",
            "ubicacion",
            "summary",
            "deadline",
            "client",
            "get_client",
            "get_client_logo",
            "exchange_rate",
            "currency",
            "status",
            "get_status_display",
            "base_amount",
            "is_archived",
            "is_deleted",
            "is_cliente_asume_combustible",
            "ratio_manpower",
            "ratio_material",
            "ratio_equipment",
            "ratio_subcontract",
            "scheduled_completion",  # plazo de la obra (meses)
            "scheduled_completion_extra",  # plazo extra de la obra (meses)
            "ratio_guarantee_faithful_compliance",  # emisión de carta de fianza de fiel cumplimiento
            "ratio2_guarantee_faithful_compliance",  # ratio 2 emisión de carta de fianza de fiel cumplimiento
            "ratio_guarantee_advance",  # ratio emisión de carta de fianza por adelanto
            "ratio2_guarantee_advance",  # ratio 2 emisión de carta de fianza por adelanto
            "ratio_civil_liability_policy",  # poliza de responsabilidad civil
            "ratio_incidentals",  # imprevistos mano de obra
            "ratio_incidentals_manpowers",  # imprevistos mano de obra
            "ratio_incidentals_equipments",  # imprevistos equipos y herramientas
            "ratio_incidentals_materials",  # imprevistos materiales
            "ratio_incidentals_subcontracts",  # imprevistos subcontratos',
            "ratio_over_head",  # gastos generales mano de obra',
            "ratio_over_head_manpowers",  # gastos generales mano de obra',
            "ratio_over_head_equipments",  # gastos generales equipos y herramientas',
            "ratio_over_head_materials",  # gastos generales materiales',
            "ratio_over_head_subcontracts",  # gastos generales subcontratos',
            "ratio_profit",  # beneficio global',
            "ratio_profit_manpowers",  # beneficio mano de obra',
            "ratio_profit_equipments",  # beneficio equipos y herramientas',
            "ratio_profit_materials",  # beneficio materiales',
            "ratio_profit_subcontracts",  # beneficio subcontratos',
            "ratio_financial_expenses",  # gastos financieros
            "ratio_itf_check_tax",  # impuesto cheque itf
            "ratio_gastos_generales_diff",
            "ratio_utilidad_diff",
            "ratio_equipo_reparacion_reposicion",  # FIXME: colocar el nombre completo de los campos
            "get_period_faithful_compliance",  # Plazo de fiel cumplimiento: Plazo de la obra + 2
            "get_period_guarantee_faithful_compliance",
            "get_period_guarantee_advance",
            "get_ratio_guarantee_faithful_compliance",
            "tree",  # Se almacena la estructura de arbol de las tareas (Actividades)
            "meses_obra",
            "meses_epp",
            "vacunas",
            # "vacuna_meses",
            "vacuna_costo",
            "vacuna_moneda",
            "ratio_manpower_gratificacion_julio_diciembre",
            "ratio_vacaciones_truncas",
            "ratio_es_salud",
            "ratio_sctr_salud",
            "ratio_sctr_pension",
            "ratio_consumo_equipos",
            "ratio_lubricante",
            "costo_examen_medico_pre_ocupacional",
            "costo_examen_medico_post_ocupacional",
            "meses_costo_certificacion",
            "nombre_gasto_1",
            "veces_gasto_1",
            "costo_gasto_1",
            "moneda_gasto_1",
            "nombre_gasto_2",
            "veces_gasto_2",
            "costo_gasto_2",
            "moneda_gasto_2",
            "catering_hoteleria_dias",
            "catering_hoteleria_costo",
            "catering_hoteleria_moneda",
            "medicina_dias",
            "medicina_costo",
            "medicina_moneda",
            "precio_gasoil",
            "precio_gasolina",
            "get_ubicacion_display",
            "get_medicina",
            "get_catering",
            "get_costo_vacunacion",
            "get_examen_medico_post_ocupacional",
            "get_examen_medico_pre_ocupacional",
            "get_gratificacion"
            # "get_current_costo_vacuna"
        )

    def create(self, validated_data):
        """
        Metodo que se ejecuta cuando se ha creado un presupuesto.
        Se crea una tarea por defecto
        """
        budget = super().create(validated_data)
        task = TaskBudget(
            budget=budget,
            wbs='0',
            outline_level=0,
            name=budget.title,
            efficiency=1.0,
            quantity= 1.0,
            projected_start_date=datetime.now().date(),
            projected_finish_date=datetime.now().date(),
            position=0,
            uid=0,
            percentage_minor_tools = 0.03,
            # apu_material_cost = 0,
            # apu_equipment_cost = 0,
            # apu_manpower_cost = 0
        )
        task.save()
        # Creamos una tarea en el arbol del presupuesto
        tree = """
        [
            {{
                "data": {{
                    "id": {0},
                    "text": "{1}",
                    "unit": null,
                    "quantity": 1,
                    "subtotal": 0,
                    "unit_subtotal": 0
                }},
                "text": "{1}"
            }}
        ]
        """.format(task.id, budget.title)
        budget.tree = tree
        budget.save(update_fields=['tree'])
        return budget


class ManpowerBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:manpowerbudget-detail",
    )

    class Meta:
        model = ManpowerBudget
        fields = (
            "id",
            "url",
            "budget",
            "manpower",
            "unit",
            "currency",
            "price",
            "quantity",
            "time_valorize",
            "type_cost",
            "epp_cost",
            "business_cost",
            "codigo",
            "puesto",
            "sueldo_bruto",
            "asignacion_familiar",
            "tipo_epp",  # Staff, Obrero...
            "certificacion",
            "relevo_trabajo",
            "relevo_descanso",
            "has_gasto_1",
            "has_gasto_2",
            "has_catering",
            "has_medicina",
            "get_tipo_epp_display",
            "get_cost_unit",
            "get_manpower_display",
            "get_manpower_name",
            "get_resource_name",
            "get_resource_code",
            "get_resource_label",
            "get_standby_hours",
            "get_standby_estimated_hours",
            "get_standby_cost",
            "get_sueldo_regular",
            "get_gratificacion_julio_diciembre",
            "get_cts_anual",
            "get_vacaciones_truncas",
            "get_es_salud",
            "get_sumatoria_1",
            "get_sctr_salud",
            "get_sctr_pension",
            "get_costo_mes_contab",
            "get_examen_medico_pre_ocupacional",
            "get_examen_medico_post_ocupacional",
            "get_epp",
            "get_costo_certificacion",
            "get_gasto_1",
            "get_gasto_2",
            "get_costo_mes_inmac",
            "get_coeficiente",
            "get_costo_mes_con_relevo",
            "get_catering",
            "get_medicina",
            "get_costo_mes_final",
            "get_personas_relevo",
            "get_epp_total",
            "get_epp_final"
        )


class MaterialBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:materialbudget-detail",
    )

    class Meta:
        model = MaterialBudget
        fields = (
            "id",
            "url",
            "budget",
            "material",
            "unit",
            "currency",
            "price",
            "type_material",
            "quantity",
            "distancia",
            "costo_unitario_transporte",
            "ratio_perdida",
            "time_valorize",
            "amortization",
            "is_deleted",
            "get_resource_name",
            "get_resource_code",
            "get_resource_label",
            "get_costo_transporte",
            "get_costo_obra",
            "get_costo_perdida",
            "get_cost_unit",
        )

class SubcontractBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:subcontractbudget-detail",
    )

    class Meta:
        model = SubcontractBudget
        fields = (
            "id",
            "url",
            "budget",
            "subcontract",
            "unit",
            "currency",
            "price",
            "quantity",
            "distancia",
            "costo_unitario_transporte",
            "ratio_perdida",
            "time_valorize",
            "amortization",
            "is_deleted",
            "get_resource_name",
            "get_resource_code",
            "get_resource_label",
            "get_costo_transporte",
            "get_costo_obra",
            "get_costo_perdida",
            "get_cost_unit",
        )

class EquipmentBudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="budget:equipmentbudget-detail",
    )

    class Meta:
        model = EquipmentBudget
        fields = (
            "id",
            "url",
            "budget",
            "equipment",
            "unit",
            "currency",
            "price",
            "category",
            "potencia",
            "quantity",
            "time_valorize",
            "hours_equipment_operation",
            "has_combustible",
            "tipo_combustible",
            "get_resource_name",
            "get_resource_code",
            "get_resource_label",
            "get_standby_hours",
            "get_standby_estimated_hours",
            "get_standby_cost",
            "get_costo_hs_alquiler",
            "get_horas_mes",
            "get_costo_mes_alquiler",
            "get_rep_resp",
            "get_costo_apu_hs_alq",
            "get_precio_combustible",
            "get_cons",
            "get_costo_combustible",
            "get_lubricante",
            "get_cost_unit",
            "get_categoria_display",
            "is_deleted",
        )