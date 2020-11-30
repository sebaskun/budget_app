# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError

from backend.core.models import FollowUserModel


# from ..project.models import Project

from django.db.models import Max, Min
from decimal import Decimal
from easy_thumbnails.exceptions import InvalidImageFormatError
# from hashid_field import HashidField

# from hashid_field import HashidAutoField

import reversion
import math

from ..core import constants, utils
from ..core.utils import CharNullField
from ..core.models import Regimen, GruposVarios, Certificado
from ..client.models import Client
from ..resource.models import (
    Manpower,
    Material,
    Equipment,
    Subcontract,
    Vacuna,
    VacunaDetail,
    CategoryEquipment,
    # OverHead
)
from decimal import Decimal

from ..utils.ceiling import ceiling

from easy_thumbnails.files import get_thumbnailer

from ..django_cloneable import CloneableMixin

site = "http://localhost:8000"

# from treebeard.mp_tree import MP_Node

TIPO_COSTO_DIRECTO = "D"
TIPO_COSTO_INDIRECTO = "I"
TIPOS_COSTO = (
    (TIPO_COSTO_DIRECTO, "DIRECTO"),
    (TIPO_COSTO_INDIRECTO, "INDIRECTO"),
)
TIPO_COSTO_DEFAULT = TIPO_COSTO_DIRECTO

User = get_user_model()


STATUS_BUDGET_CANCELED = "CA"
STATUS_BUDGET_NEW = "NW"
STATUS_BUDGET_SURPASSED = "SU"
STATUS_BUDGET_TOCONFIRM = "TC"
STATUS_BUDGET_UNDATE = "UD"
STATUS_BUDGET_WAITING = "WA"

STATUS_BUDGET = (
    (STATUS_BUDGET_WAITING, "pendiente"),
    (STATUS_BUDGET_NEW, "nuevo"),
    (STATUS_BUDGET_SURPASSED, "superado"),
    (STATUS_BUDGET_CANCELED, "cancelado"),
    (STATUS_BUDGET_TOCONFIRM, "por confirmar"),
    (STATUS_BUDGET_UNDATE, "sin fecha"),
)

STATUS_BUDGET_DEFAULT = STATUS_BUDGET_NEW


@reversion.register()
class Budget(FollowUserModel):
    """
    Presupuesto
    """
    # id = HashidAutoField(primary_key=True)
    code = CharNullField(
        verbose_name='código',
        max_length=15,
        blank=True,
        null=True
    )
    client = models.ForeignKey(
        Client,
        verbose_name="cliente",
        related_name="clients",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    title = models.TextField(
        'Titulo',
        blank=False,
        null=False,
        default="Sin título"
    )
    location = CharNullField(
        verbose_name='Locación',
        max_length=150,
        blank=True,
        null=True
    )
    ubicacion = models.ForeignKey(
        GruposVarios,
        verbose_name="ubicacion",
        related_name="ubicacion_presupuesto",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'grupo': constants.GRUPO_UBICACION}
    )
    summary = models.TextField(
        'Resumen',
        blank=True,
        null=True,
    )
    exchange_rate = models.DecimalField(
        verbose_name='tipo de cambio',
        max_digits=10, decimal_places=3,
        blank=False,
        null=False,
        default=Decimal("1.000")
    )
    base_amount = models.DecimalField(
        'importe base',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=Decimal("0.00")
    )
    deadline = models.DateField(
        verbose_name='fecha límite',
        blank=True,
        null=True,
    )
    currency = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    status = models.CharField(
        'estado',
        max_length=2,
        blank=False,
        null=False,
        choices=STATUS_BUDGET,
        default=STATUS_BUDGET_DEFAULT
    )
    position = models.PositiveIntegerField(
        'posición',
        default=0,
        blank=False,
        null=False
    )
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Desde aquí datos para el costeo de mano de obra
    workdays_per_month = models.DecimalField(
        verbose_name='días laborables por mes',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=30
    )
    normal_working_hours = models.DecimalField(
        verbose_name='horas laborables del día',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=8
    )
    ratio_manpower = models.DecimalField(
        verbose_name='coeficiente de paso de mano de obra',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_material = models.DecimalField(
        verbose_name='coeficiente de paso de material',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_equipment = models.DecimalField(
        verbose_name='coeficiente de paso de equipo',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=Decimal('1.00')
    )
    ratio_equipo_reparacion_reposicion = models.DecimalField(
        verbose_name='ratio de equipos rep resp',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('15.00')
    )
    ratio_lubricante = models.DecimalField(
        verbose_name='ratio del lubricante',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('20.00')
    )
    ratio_subcontract = models.DecimalField(
        verbose_name='coeficiente de paso de subcontrato',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    scheduled_completion = models.DecimalField(
        verbose_name='plazo de la obra (meses)',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=1
    )
    scheduled_completion_extra = models.DecimalField(
        verbose_name='plazo extra de la obra (meses)',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=2
    )
    ratio_guarantee_faithful_compliance = models.DecimalField(
        verbose_name='emisión de carta de fianza de fiel cumplimiento',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_guarantee_advance = models.DecimalField(
        verbose_name='emisión de carta de fianza por adelanto',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio2_guarantee_faithful_compliance = models.DecimalField(
        verbose_name='emisión de carta de fianza de fiel cumplimiento',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio2_guarantee_advance = models.DecimalField(
        verbose_name='emisión de carta de fianza por adelanto',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_civil_liability_policy = models.DecimalField(
        verbose_name='poliza de responsabilidad civil',
        max_digits=9, decimal_places=6,
        blank=False,
        null=False,
        default=1
    )
    ratio_incidentals_manpowers = models.DecimalField(
        verbose_name='imprevistos mano de obra',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_incidentals_equipments = models.DecimalField(
        verbose_name='imprevistos equipos y herramientas',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_incidentals_materials = models.DecimalField(
        verbose_name='imprevistos materiales',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_incidentals_subcontracts = models.DecimalField(
        verbose_name='imprevistos subcontratos',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_incidentals = models.DecimalField(
        verbose_name='ratio_imprevistos',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_over_head_manpowers = models.DecimalField(
        verbose_name='gastos generales mano de obra',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_over_head_equipments = models.DecimalField(
        verbose_name='gastos generales equipos y herramientas',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_over_head_materials = models.DecimalField(
        verbose_name='gastos generales materiales',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_over_head_subcontracts = models.DecimalField(
        verbose_name='gastos generales subcontratos',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_over_head = models.DecimalField(
        verbose_name='porcentaje gastos generales',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_profit_manpowers = models.DecimalField(
        verbose_name='beneficio mano de obra',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_profit_equipments = models.DecimalField(
        verbose_name='beneficio equipos y herramientas',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_profit_materials = models.DecimalField(
        verbose_name='beneficio materiales',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_profit_subcontracts = models.DecimalField(
        verbose_name='beneficio subcontratos',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_profit = models.DecimalField(
        verbose_name='beneficio',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_financial_expenses = models.DecimalField(
        verbose_name='gastos financieros',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_itf_check_tax = models.DecimalField(
        verbose_name='impuesto cheque itf',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=1
    )
    ratio_gastos_generales_diff = models.DecimalField(
        verbose_name='gastos generales diferenciado',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=0
    )
    ratio_utilidad_diff = models.DecimalField(
        verbose_name='utilidad diferenciado',
        max_digits=8, decimal_places=5,
        blank=False,
        null=False,
        default=0
    )
    tree = JSONField(
        'arbol',
        blank=True,
        null=True
    )
    meses_obra = models.DecimalField(
        verbose_name='meses de obra',
        max_digits=5, decimal_places=2,
        blank=True,
        null=True,
        default=0
    )
    meses_epp = models.DecimalField(
        verbose_name='meses de epp',
        max_digits=5, decimal_places=2,
        blank=True,
        null=True,
        default=0
    )
    vacunas = models.ForeignKey(
        Vacuna,
        verbose_name="vacunas",
        related_name="vacunas_budget",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    vacuna_costo = models.DecimalField(
        verbose_name='costo de vacuna',
        max_digits=6, decimal_places=2,
        blank=True,
        null=True,
        default=0
    )
    vacuna_moneda = models.CharField(
        'moneda vacunas',
        max_length=1,
        blank=True,
        null=True,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    ratio_manpower_gratificacion_julio_diciembre = models.DecimalField(
        verbose_name='ratio de mano de obra de gratificacion julio - diciembre',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('9.00')
    )
    ratio_vacaciones_truncas = models.DecimalField(
        verbose_name='ratio de vacaciones truncas',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('8.33')
    )
    ratio_es_salud = models.DecimalField(
        verbose_name='ratio de essalud',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('9.00')
    )
    ratio_sctr_salud = models.DecimalField(
        verbose_name='ratio de sctr salud',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('1.00')
    )
    ratio_sctr_pension = models.DecimalField(
        verbose_name='ratio de sctr pension',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('1.00')
    )
    costo_examen_medico_pre_ocupacional = models.DecimalField(
        verbose_name='costo de examen medico pre-ocupacional',
        max_digits=10, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('429.55')
    )
    costo_examen_medico_post_ocupacional = models.DecimalField(
        verbose_name='costo de examen medico post-ocupacional',
        max_digits=10, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('193.00')
    )
    meses_costo_certificacion = models.DecimalField(
        verbose_name='meses de costo de certificacion',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    nombre_gasto_1 = models.CharField(
        verbose_name='nombre gasto 1',
        max_length=50,
        blank=True,
        null=True,
    )
    veces_gasto_1 = models.PositiveSmallIntegerField(
        verbose_name='veces gasto 1',
        blank=True,
        null=True,
    )
    costo_gasto_1 = models.DecimalField(
        verbose_name='costo gasto 1',
        max_digits=10, decimal_places=2,
        blank=True,
        null=True,
    )
    moneda_gasto_1 = models.CharField(
        ' moneda gasto 1',
        max_length=1,
        blank=True,
        null=True,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    nombre_gasto_2 = models.CharField(
        verbose_name='nombre gasto 2',
        max_length=50,
        blank=True,
        null=True,
    )
    veces_gasto_2 = models.PositiveSmallIntegerField(
        verbose_name='veces gasto 2',
        blank=True,
        null=True,
    )
    costo_gasto_2 = models.DecimalField(
        verbose_name='costo gasto 2',
        max_digits=10, decimal_places=2,
        blank=True,
        null=True,
    )
    moneda_gasto_2 = models.CharField(
        'moneda gasto 2',
        max_length=1,
        blank=True,
        null=True,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    catering_hoteleria_dias = models.PositiveSmallIntegerField(
        verbose_name='numero de dias de catering hoteleria',
        blank=True,
        null=True,
        default=30
    )
    catering_hoteleria_costo = models.DecimalField(
        verbose_name='costo de catering - hoteleria',
        max_digits=10, decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    catering_hoteleria_moneda = models.CharField(
        'moneda catering',
        max_length=1,
        blank=True,
        null=True,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    medicina_dias = models.PositiveSmallIntegerField(
        verbose_name='numero de dias de medicina',
        blank=True,
        null=True,
        default=30
    )
    medicina_costo = models.DecimalField(
        verbose_name='costo de medicina',
        max_digits=10, decimal_places=2,
        blank=True,
        null=True,
        default=0
    )
    medicina_moneda = models.CharField(
        'moneda medicina',
        max_length=1,
        blank=True,
        null=True,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    is_cliente_asume_combustible = models.BooleanField(default=True)
    
    precio_gasoil = models.DecimalField(
        'precio del gasoil',
        max_digits=5, decimal_places=3,
        blank=False,
        null=False,
        default=Decimal('1.1')
    )
    precio_gasolina = models.DecimalField(
        'precio del gasolina',
        max_digits=5, decimal_places=3,
        blank=False,
        null=False,
        default=Decimal('1.1')
    )
    ratio_consumo_equipos = models.DecimalField(
        'consumo de equipos',
        max_digits=3, decimal_places=2,
        blank=False,
        null=False,
        default=Decimal('0.11')
    )

    def __str__(self):
        return "{} {}".format(self.code, self.title)

    class Meta:
        ordering = ('-created',)
        verbose_name = "presupuesto"
        verbose_name_plural = "presupuestos"
        permissions = (
            ("can_add_budget", "Puede adicionar presupuesto"),
            ("can_edit_budget", "Puede modificar presupuesto"),
            ("can_change_status_budget", "Puede cambiar estado presupuesto"),
            ("can_see_view_budget", "Puede ver presupuesto"),
        )

    # def full_clean(self):
    #     print("grupo", self.ubicacion.grupo)
    #     if self.ubicacion.grupo != constants.GRUPO_UBICACION:
    #         raise ValidationError({'ubicacion': "El grupo tiene que ser una ubicación"})

    @property
    def get_ubicacion_display(self):
        """
        Ubicación
        """
        if self.ubicacion:
            return self.ubicacion.nombre
        return None

    @property
    def get_medicina(self):
        """
        Medicina
        """
        if self.medicina_costo:
            return self.medicina_costo * self.medicina_dias
        return 0

    @property
    def get_catering(self):
        """
        Catering Hoteleria
        """
        if self.catering_hoteleria_costo:
            catering = self.catering_hoteleria_costo * self.catering_hoteleria_dias
            if self.catering_hoteleria_moneda == "D":
                catering = catering * self.exchange_rate
            return catering
        return 0

    @property
    def get_costo_vacunacion(self):
        """
        Costo Vacunacion
        """
        if self.meses_obra == 0:
            return 0
        return self.vacuna_costo / self.meses_obra

    # @property
    # def get_current_costo_vacuna(self):
    #     if self.vacunas:
    #         costo = self.vacunas.get_costo_vacuna
    #         if self.currency == "D":
    #             costo = costo / self.exchange_rate
    #         return costo
    #     return None

    @property
    def get_examen_medico_post_ocupacional(self):
        """
        Examen medico post-ocupacional
        """
        if self.meses_obra == 0:
            return 0
        return self.costo_examen_medico_post_ocupacional / self.meses_obra

    @property
    def get_examen_medico_pre_ocupacional(self):
        """
        Examen medico pre-ocupacional
        """
        if self.meses_obra == 0:
            return 0
        return self.costo_examen_medico_pre_ocupacional / self.meses_obra

    @property
    def get_gratificacion(self):
        """
        Gratificacion
        """
        return Decimal(1 / 12) * 2 * (
            1 + (self.ratio_manpower_gratificacion_julio_diciembre / 100))

    @property
    def get_period_faithful_compliance(self):
        """
        Plazo de fiel cumplimiento: Plazo de la obra + 2
        """
        if self.scheduled_completion:
            return self.scheduled_completion + self.scheduled_completion_extra
        return 0

    @property
    def get_period_guarantee_faithful_compliance(self):
        """
        Periodo de Fianza de Fiel Cumplimiento
        """
        return ceiling(self.get_period_faithful_compliance, 3)

    @property
    def get_period_guarantee_advance(self):
        """
        Periodo de Fianza por Adelanto
        """
        return ceiling(self.scheduled_completion, 3)

    @property
    def get_ratio_guarantee_faithful_compliance(self):
        """
        Calcula el ratio global para la carta fianza de fiel cumplimiento
        """
        return (
            self.ratio_guarantee_faithful_compliance *
            self.ratio2_guarantee_faithful_compliance *
            self.get_period_faithful_compliance
        )

    @property
    def get_ratio_guarantee_advance(self):
        """
        Calcula el ratio global para la carta fianza de fiel cumplimiento
        """
        return (
            self.ratio_guarantee_advance *
            self.get_period_guarantee_advance *
            self.ratio2_guarantee_advance
        )

    @property
    def get_task_cost(self):
        return (
            self.apu_manpower_cost +
            self.apu_material_cost +
            self.apu_equipment_cost +
            self.apu_minus_tools_cost
        )

    @property
    def get_pk(self):
        # return self.id.hashid
        return self.id

    @property
    def get_client(self):
        if self.client:
            return self.client.get_short_name
        return None

    @property
    def get_client_logo(self):
        if bool(self.client.logo):
            return self.client.logo.url
        else:
            return None

    @property
    def get_image_miniature_50_0(self):
        if bool(self.client.logo):
            try:
                return get_thumbnailer(self.client.logo)['miniature_50_0'].url
            except InvalidImageFormatError:
                return ""

    @property
    def get_total(self):
        total = 0
        for item in self.tasks_budget.all():
            total += item.get_subtotal
        return total

    @property
    def get_standby_total_materials(self):
        total = 0
        for item in self.materials_budget.all():
            total += item.get_standby_subtotal_material
        return total

    # @property
    # def get_project_name(self):
    #     return self.proyecto.nombre

    # @property
    # def get_project_shortname(self):
    #     return self.proyecto.nombre_corto

    # @property
    # def get_client_name(self):
    #     return self.proyecto.cliente.nombre

    # @property
    # def get_status_name(self):
    #     return self.get_status_display
    def save(self, *args, **kwargs):
        if not self.code:
            client = self.client
            if client:
                self.code = utils.get_correlative(
                    constants.MODELO_PRESUPUESTO,
                    client.initials,
                    3)
        super(Budget, self).save(*args, **kwargs)

    @property
    def get_date_max(self):
        tasks = self.tasks_budget.all()
        if tasks:
            return tasks.aggregate(Max('projected_finish_date'))

        return None

    @property
    def get_date_min(self):
        tasks = self.tasks_budget.all()
        if tasks:
            return tasks.aggregate(Min('projected_start_date'))

        return None

    def fix_tasks(self):
        tasks = self.tasks_budget.all().order_by('position', 'wbs', '-id')
        wbs = [0]
        position = 0
        prev = None
        for task in tasks:
            task.position = position
            position = position+1

            prev_level = prev.outline_level if prev else 0
            level = task.outline_level

            for index in range(prev_level, level, 1):
                wbs.append(0)
            for index in range(prev_level, level, -1):
                del wbs[-1]
            if prev_level == 0 and level == 1:
                del wbs[-1]
            else:
                wbs[-1] = wbs[-1]+1

            task.wbs = ".".join(str(x) for x in wbs)
            if task.position == 0:
                task.wbs = '0'
            prev = task
            task.save()


@reversion.register()
class TaskBudget(FollowUserModel):
    """
    Tarea
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name="presupuesto",
        related_name="tasks_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    wbs = models.CharField(
        'EDT',
        max_length=50,
        blank=False,
        null=False,
    )
    outline_level = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        default=0
    )
    name = models.CharField(
        'nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    unit = models.CharField(
        'unidad',
        max_length=15,
        blank=True,
        null=True,
    )
    efficiency = models.DecimalField(
        'rendimiento',
        max_digits=15, decimal_places=6,
        blank=True,
        null=True,
        default=1
    )
    efficiency_divider = models.DecimalField(
        'rendimiento divisor',
        max_digits=15, decimal_places=6,
        blank=True,
        null=True,
        default=1
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=True,
        null=True,
        default=1
    )
    projected_start_date = models.DateField(
        verbose_name='inicio',
        blank=True,
        null=True,
    )
    projected_finish_date = models.DateField(
        verbose_name='término',
        blank=True,
        null=True,
    )
    position = models.PositiveIntegerField(
        'posición',
        blank=False,
        null=False,
        default=0
    )
    uid = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=0
    )
    percentage_minor_tools = models.DecimalField(
        'porcentaje de herramientas menores',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0.03
    )
    is_parent = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):              # __unicode__ on Python 2
        code = self.budget.code
        return "{} - {} {}".format(code, self.wbs, self.name)

    class Meta:
        verbose_name = "tarea por presupuesto"
        verbose_name_plural = "tareas por presupuesto"
        ordering = ('budget', 'position',)

    @property
    def text(self):
        return self.name

    @property
    def data(self):
        context = {
            "id": self.id,
            "text": self.name,
            "unit": self.unit,
            "quantity": self.quantity,
            "unit_subtotal": self.get_unit_subtotal,
            "subtotal": self.get_subtotal
        }
        return context

    @property
    def get_efficiency(self):
        # if self.efficiency_divider > 0:
        #     return self.efficiency / self.efficiency_divider
        return self.efficiency

    @property
    def get_subtotal_manpower(self):
        subtotal = 0
        for item in self.tasks_manpower_task.all():
            subtotal += item.get_subtotal
        return subtotal

    @property
    def get_subtotal_material(self):
        subtotal = 0
        for item in self.tasks_material_task.all():
            subtotal += item.get_subtotal
        return subtotal

    @property
    def get_subtotal_equipment(self):
        subtotal = 0
        for item in self.tasks_equipment_task.all():
            subtotal += item.get_subtotal
        return subtotal

    @property
    def get_subtotal_subcontract(self):
        subtotal = 0
        for item in self.tasks_subcontract_task.all():
            subtotal += item.get_subtotal
        return subtotal

    @property
    def get_subtotal_minor_tools(self):
        return round(
            self.get_subtotal_manpower *
            self.percentage_minor_tools, 2)

    @property
    def get_unit_subtotal(self):
        return (
            self.get_subtotal_equipment +
            self.get_subtotal_manpower +
            self.get_subtotal_material +
            self.get_subtotal_subcontract + 
            self.get_subtotal_minor_tools
        )

    @property
    def get_subtotal(self):
        return round(self.get_unit_subtotal * self.quantity, 2)

    # @property
    # def get_apu_minor_tools_cost(self):
    #     subtotal = self.apu_manpower_cost * self.percentage_minor_tools
    #     return subtotal

    @property
    def get_outline_level(self):
        if self.wbs:
            return self.wbs.count(".") + 1
        else:
            return 0

    @property
    def get_diff_dates(self):
        """
        Devuelve la diferencia de horas
        """
        if self.projected_start_date and self.projected_finish_date:
            diff = self.projected_finish_date - self.projected_start_date
            return diff.days
        return 0

    @property
    def get_diff_dates_formatted(self, hours_per_day=8):
        """
        Devuelve la diferencia de fechas pero en formato de horas para
        ms project
        """
        days = self.get_diff_dates * hours_per_day
        return "PT{}H0M0S".format(days)


class ResourceBudgetBase(FollowUserModel):
    unit = models.CharField(
        verbose_name='unidad de costo',
        max_length=15,
        blank=True,
        null=True,
        default="Hr"
    )
    currency = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    price = models.DecimalField(
        'precio',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    position = models.PositiveIntegerField(
        'posición',
        blank=False,
        null=False,
        default=0
    )
    allows_ratio = models.PositiveIntegerField(
        'Permite coeficiente?',
        blank=False,
        null=False,
        default=1
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


@reversion.register()
class CertificacionBudget(FollowUserModel):
    """
    Presupuesto de certificacion
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name="presupuesto",
        related_name="certificaciones_budget",
        on_delete=models.CASCADE
    )
    certificado = models.ForeignKey(
        Certificado,
        verbose_name='certificado',
        related_name="certificacion_certificado",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    moneda = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    importe = models.DecimalField(
        'importe',
        max_digits=8, decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ("id",)
        unique_together = (("budget", "certificado"))

    @property
    def get_certificado_display(self):
        if self.certificado:
            return self.certificado.nombre
        return ""

    def __str__(self):
        return self.get_certificado_display


@reversion.register()
class ManpowerBudget(ResourceBudgetBase):
    """
    Precios base de la mano de obra de un presupuesto
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name=u'Presupuesto',
        related_name="manpowers_budget",
        on_delete=models.CASCADE
    )
    manpower = models.ForeignKey(
        Manpower,
        verbose_name="mano de obra",
        related_name="manpowers_manpower_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    time_valorize = models.DecimalField(
        'tiempo a valorizar',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    business_cost = models.DecimalField(
        'costo empresarial',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    epp_cost = models.DecimalField(
        'costo de epp',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    type_cost = models.CharField(
        'tipo de costo',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.TYPE_COST,
        default=constants.TYPE_COST_DEFAULT
    )
    codigo = models.CharField(
        'codigo',
        max_length=5,
        blank=True,
        null=True,
    )
    puesto = models.CharField(
        'puesto',
        max_length=150,
        blank=True,
        null=True,
    )
    sueldo_bruto = models.DecimalField(
        'sueldo bruto',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    asignacion_familiar = models.DecimalField(
        'asignacion familiar',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=93
    )
    
    tipo_epp = models.ForeignKey(
        GruposVarios,
        verbose_name="tipo de epp",
        related_name="tipo_epps_manpower_grupo",
        on_delete=models.CASCADE,
        blank=True,  # Este debe ser False. Dato obligatorio
        null=True,   # Este debe ser False. Dato obligatorio
        limit_choices_to={'grupo': constants.GRUPO_TIPO_EPP}
    )
    certificacion = models.ForeignKey(
        CertificacionBudget,
        verbose_name="certificacion",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    relevo_trabajo = models.DecimalField(
        'relevo trabajo',
        max_digits=4,
        decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    relevo_descanso = models.DecimalField(
        'relevo descanso',
        max_digits=4,
        decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    has_gasto_1 = models.BooleanField(default=False)
    has_gasto_2 = models.BooleanField(default=False)
    has_catering = models.BooleanField(default=False)
    has_medicina = models.BooleanField(default=True)

    def __str__(self):
        return self.manpower.name

    class Meta:
        verbose_name = "mano de obra"
        verbose_name_plural = "manos de obra"
        ordering = ('manpower__code', 'manpower__name')
        unique_together = (("budget", "manpower"))

    @property
    def get_personas_relevo(self):
        formato = "{}x{};{}".format(int(self.relevo_trabajo), int(self.relevo_descanso), int(self.quantity))
        # print("formato:", formato)
        try:
            return constants.REGIMEN[formato]
        except:
            return 0

    @property
    def get_sueldo_regular(self):
        return self.sueldo_bruto + self.asignacion_familiar
    
    @property
    def get_gratificacion_julio_diciembre(self):
        return self.get_sueldo_regular * self.budget.get_gratificacion
    
    @property
    def get_cts_anual(self):
        return ((Decimal(self.get_gratificacion_julio_diciembre / Decimal(1.09)) / 6) + self.sueldo_bruto)/12
    
    @property
    def get_vacaciones_truncas(self):
        return self.get_sueldo_regular * self.budget.ratio_vacaciones_truncas / 100

    @property
    def get_es_salud(self):
        return (
            (self.get_sueldo_regular + self.get_vacaciones_truncas) *
            self.budget.ratio_es_salud / 100
        )
    
    @property
    def get_sumatoria_1(self):
        return ( 
            self.get_sueldo_regular +
            self.get_gratificacion_julio_diciembre +
            self.get_cts_anual +
            self.get_vacaciones_truncas +
            self.get_es_salud
        )

    @property
    def get_sctr_salud(self):
        return self.get_sumatoria_1 * self.budget.ratio_sctr_salud / 100
        
    @property
    def get_sctr_pension(self):
        return self.get_sumatoria_1 * self.budget.ratio_sctr_pension / 100
    
    @property
    def get_costo_mes_contab(self):
        return (
            self.get_sumatoria_1 +
            self.get_sctr_salud + 
            self.get_sctr_pension
        )

    @property
    def get_examen_medico_pre_ocupacional(self):
        return self.budget.get_examen_medico_pre_ocupacional

    @property
    def get_examen_medico_post_ocupacional(self):
        return self.budget.get_examen_medico_post_ocupacional

    @property
    def get_epp(self):
        result = self.budget.epps_budget.filter(tipo_epp=self.tipo_epp)
        if result.count() > 0:
            return result[0].get_costo_mes
        return 0

    @property
    def get_tipo_epp_display(self):
        if self.tipo_epp:
            return self.tipo_epp.nombre
        return None

    @property
    def get_costo_certificacion(self):
        if self.budget.meses_costo_certificacion == 0 or self.certificacion == None:
            return 0

        currency = self.certificacion.moneda
        exchange = self.budget.exchange_rate

        costo = self.certificacion.importe / self.budget.meses_costo_certificacion
        if currency == "D":
            costo = costo * exchange
        return costo

    @property
    def get_gasto_1(self):
        if self.has_gasto_1:
            # if self.budget.veces_gasto_1 == None or self.budget.costo_gasto_1 == None:
            #     return 0
            return (self.budget.veces_gasto_1 or 0) * (self.budget.costo_gasto_1 or 0)
        return 0
            
    @property
    def get_gasto_2(self):
        if self.has_gasto_2:
            # return self_budget
            # if self.budget.veces_gasto_2 == None or self.budget.costo_gasto_2 == None:
            #     return 0
            return (self.budget.veces_gasto_2 or 0) * (self.budget.costo_gasto_2 or 0)
        return 0
            
    @property
    def get_costo_mes_inmac(self):
        return (
            self.get_costo_mes_contab +
            self.get_examen_medico_pre_ocupacional +
            self.get_examen_medico_post_ocupacional +
            self.budget.get_costo_vacunacion + 
            self.get_epp + 
            self.get_costo_certificacion +
            self.get_gasto_1 + self.get_gasto_2
        )
            
    @property
    def get_coeficiente(self):
        if self.relevo_trabajo == 0:
            return 0
        return round((self.relevo_trabajo + self.relevo_descanso) / self.relevo_trabajo, 2)
            
    @property
    def get_costo_mes_con_relevo(self):
        return self.get_costo_mes_inmac * self.get_coeficiente
            
    @property
    def get_catering(self):
        if self.has_catering:
            return self.budget.get_catering
        return 0
    
    @property
    def get_medicina(self):
        if self.has_medicina:
            return self.budget.get_medicina
        return 0
            
    @property
    def get_costo_mes_final(self):
        return (
            self.get_costo_mes_con_relevo +
            self.get_catering +
            self.get_medicina
        )

    @property
    def get_standby_hours(self):
        quantity = 0
        for item in self.manpowers_budget_manpower_task.all():
            quantity += round(
                item.task.quantity *
                item.get_efficiency * item.quantity, 2)
        return quantity

    @property
    def get_standby_estimated_hours(self):
        return (
            self.quantity *
            self.time_valorize *
            self.budget.workdays_per_month *
            self.budget.normal_working_hours
        )

    @property
    def get_standby_cost(self):
        delta = self.get_standby_estimated_hours - self.get_standby_hours
        if delta > 0:
            return delta * self.get_cost_unit
        return 0.0

    @property
    def get_overhead_cost(self):
        return (
            self.quantity *
            self.time_valorize *
            self.get_business_cost
        )

    @property
    def get_standby_hydration(self):
        return (
            self.quantity *
            self.time_valorize *
            Decimal(3.5 / 20) *
            self.budget.workdays_per_month
        )

    @property
    def get_standby_epp(self):
        return (
            self.quantity *
            self.time_valorize *
            self.get_epp /
            self.budget.exchange_rate if self.budget.currency == "D" else 1
        )

    @property
    def get_epp_total(self):
        result = self.budget.epps_budget.filter(tipo_epp=self.tipo_epp)
        if result.count() > 0:
            if self.type_cost == "D":  # Directo 
                costo = result[0].get_costo
            else:  # Indirecto
                costo = result[0].get_costo_mes
            if self.budget.currency == "D":  # Dólares
                return costo / self.budget.exchange_rate
            return costo
        return 0

    @property
    def get_epp_final(self):
        if self.type_cost == "I":  # Indirecto
            q = self.quantity * self.time_valorize
        else:
            q = self.get_personas_relevo
        return self.get_epp_total * q


    @property
    def get_cost_unit(self):
        hours = self.budget.normal_working_hours
        ratio = self.budget.ratio_manpower
        days = self.budget.workdays_per_month
        exchange = self.budget.exchange_rate
        currency = self.budget.currency

        cost = self.get_costo_mes_final / (hours * days)
        if self.allows_ratio == 1:
            cost = cost * ratio

        if currency == "D" and self.currency == "S":
            cost = cost / exchange
        elif currency == "S" and self.currency == "D":
            cost = cost * exchange

        return cost

    @property
    def get_business_cost(self):
        ratio = self.budget.ratio_manpower
        exchange = self.budget.exchange_rate
        currency = self.budget.currency

        cost = self.get_costo_mes_final
        if self.allows_ratio == 1:
            cost = cost * ratio
            
        if currency == "D":
            cost = cost / exchange

        return cost

    # @property
    # def get_epp_cost(self):
    #     cost = self.epp_cost
    #     exchange = self.budget.exchange_rate
    #     currency = self.budget.currency

    #     if currency == "D" and self.currency == "S":
    #         cost = cost / exchange
    #     elif currency == "S" and self.currency == "D":
    #         cost = cost * exchange

    #     return cost

    @property
    def get_resource_name(self):
        return self.manpower.name

    @property
    def get_resource_code(self):
        return self.manpower.code

    @property
    def get_manpower_display(self):
        return "{0} - {1} ({2})".format(
            self.manpower.code or '--',
            self.manpower.name,
            self.manpower.unit)

    @property
    def get_manpower_name(self):
        return "{0} - {1} ({2})".format(
            self.manpower.code,
            self.manpower.name,
            self.manpower.unit)

    @property
    def get_resource_label(self):
        return "{0} - {1}".format(
            self.manpower.code,
            self.manpower.name)

    @property
    def get_manpower_id(self):
        return self.manpower.id

    
@reversion.register()
class MaterialBudget(ResourceBudgetBase):
    """
    Precios base del material de un presupuesto
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name=u'Presupuesto',
        related_name="materials_budget",
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material,
        verbose_name="material",
        related_name="materials_material_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    type_material = models.CharField(
        'tipo de material',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.TYPE_MATERIAL,
        default=constants.TYPE_MATERIAL_DEFAULT
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    time_valorize = models.DecimalField(
        'tiempo a valorizar',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    amortization = models.DecimalField(
        'amortización',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    is_subcontract = models.BooleanField(default=False)
    distancia = models.DecimalField(
        'distancia',
        max_digits=8, decimal_places=3,
        blank=True,
        null=True,
    )
    costo_unitario_transporte = models.DecimalField(
        'costo unitario de transporte',
        max_digits=9, decimal_places=4,
        blank=True,
        null=True,
    )
    ratio_perdida = models.DecimalField(
        'ratio de perdida',
        max_digits=5, decimal_places=2,
        blank=True,
        null=True,
        default=Decimal("1.00")
    )

    def __str__(self):
        return self.material.name

    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"
        # ordering = ("code", "name")
        unique_together = (("budget", "material"))

    @property
    def get_costo_transporte(self):
        if self.distancia and self.costo_unitario_transporte:
            return self.distancia * self.costo_unitario_transporte
        return 0
    
    @property
    def get_costo_obra(self):
        return self.price + self.get_costo_transporte

    @property
    def get_costo_perdida(self):
        if self.ratio_perdida:
            return self.get_costo_obra * self.ratio_perdida / 100
        return 0

    @property
    def get_cost_unit(self):
        ratio = self.budget.ratio_material
        exchange = self.budget.exchange_rate
        currency = self.budget.currency

        cost = (self.get_costo_obra + self.get_costo_perdida) * self.budget.ratio_material
        if currency == "D" and self.currency == "S":
            cost = cost / exchange
        elif currency == "S" and self.currency == "D":
            cost = cost * exchange

        return cost

    @property
    def get_overhead_cost(self):
        return (
            self.quantity *
            self.time_valorize *
            self.get_cost_unit *
            (self.amortization or 1)
        )

    @property
    def get_resource_name(self):
        return self.material.name

    @property
    def get_resource_code(self):
        return self.material.code

    @property
    def get_resource_label(self):
        return "{0} - {1} ({2})".format(
            self.material.code,
            self.material.name,
            self.unit)

    @property
    def get_resource_id(self):
        return self.material.id


@reversion.register()
class SubcontractBudget(ResourceBudgetBase):
    """
    Precios base del subcontrato de un presupuesto
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name=u'Presupuesto',
        related_name="subcontracts_budget",
        on_delete=models.CASCADE
    )
    subcontract = models.ForeignKey(
        Subcontract,
        verbose_name="subcontrato",
        related_name="subcontracts_subcontract_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    time_valorize = models.DecimalField(
        'tiempo a valorizar',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    amortization = models.DecimalField(
        'amortización',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    distancia = models.DecimalField(
        'distancia',
        max_digits=8, decimal_places=3,
        blank=True,
        null=True,
    )
    costo_unitario_transporte = models.DecimalField(
        'costo unitario de transporte',
        max_digits=9, decimal_places=4,
        blank=True,
        null=True,
    )
    ratio_perdida = models.DecimalField(
        'ratio de perdida',
        max_digits=5, decimal_places=2,
        blank=True,
        null=True,
        default=Decimal("1.00")
    )

    def __str__(self):
        return self.subcontract.name

    class Meta:
        verbose_name = "subcontrato"
        verbose_name_plural = "subcontratos"
        # ordering = ("code", "name")
        unique_together = (("budget", "subcontract"))

    @property
    def get_costo_transporte(self):
        if self.distancia and self.costo_unitario_transporte:
            return self.distancia * self.costo_unitario_transporte
        return 0
    
    @property
    def get_costo_obra(self):
        return self.price + self.get_costo_transporte

    @property
    def get_costo_perdida(self):
        if self.ratio_perdida:
            return self.get_costo_obra * self.ratio_perdida / 100
        return 0

    @property
    def get_cost_unit(self):
        ratio = self.budget.ratio_subcontract
        exchange = self.budget.exchange_rate
        currency = self.budget.currency

        cost = (self.get_costo_obra + self.get_costo_perdida) * self.budget.ratio_subcontract
        if currency == "D" and self.currency == "S":
            cost = cost / exchange
        elif currency == "S" and self.currency == "D":
            cost = cost * exchange

        return cost

    @property
    def get_overhead_cost(self):
        return (
            self.quantity *
            self.time_valorize *
            self.get_cost_unit *
            (self.amortization or 1)
        )

    @property
    def get_resource_name(self):
        return self.subcontract.name

    @property
    def get_resource_code(self):
        return self.subcontract.code

    @property
    def get_resource_label(self):
        return "{0} - {1} ({2})".format(
            self.subcontract.code,
            self.subcontract.name,
            self.subcontract.unit)

    @property
    def get_resource_id(self):
        return self.subcontract.id


@reversion.register()
class EquipmentBudget(ResourceBudgetBase):
    """
    Precios base del equipo de un presupuesto
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name=u'Presupuesto',
        related_name="equipments_budget",
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        Equipment,
        verbose_name="equipo",
        related_name="equipments_equipment_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        CategoryEquipment,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    potencia = models.DecimalField(
        'potencia del equipo',
        max_digits=6, decimal_places=2,
        blank=True,
        null=True,
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    time_valorize = models.DecimalField(
        'tiempo a valorizar',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    hours_equipment_operation = models.DecimalField(
        'horas de operación del equipo',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=8.00
    )
    has_combustible = models.BooleanField(default=False)
    tipo_combustible = models.CharField(
        'tipo de combustible',
        max_length=2,
        blank=True,
        null=True,
        choices=constants.COMBUSTIBLE,
    )

    def __str__(self):
        return self.equipment.name

    class Meta:
        verbose_name = "equipo"
        verbose_name_plural = "equipos"
        ordering = ("position",)
        unique_together = (("budget", "equipment"))

    @property
    def get_categoria_display(self):
        return self.equipment.get_category_display

    @property
    def get_costo_hs_alquiler(self):
        return self.price*self.budget.ratio_equipment
    
    @property
    def get_horas_mes(self):
        return self.hours_equipment_operation * self.budget.workdays_per_month

    @property
    def get_costo_mes_alquiler(self):
        return self.get_costo_hs_alquiler * self.get_horas_mes

    @property
    def get_rep_resp(self):
        return self.get_costo_hs_alquiler * self.budget.ratio_equipo_reparacion_reposicion / 100

    @property
    def get_costo_apu_hs_alq(self):
        return self.get_costo_hs_alquiler + self.get_rep_resp

    @property
    def get_precio_combustible(self):
        combustible = 0
        if self.tipo_combustible:
            if self.tipo_combustible == 'GS':
                combustible = self.budget.precio_gasolina
            else:
                combustible = self.budget.precio_gasoil
            if self.currency == "S":
                combustible = combustible * self.budget.exchange_rate
        return combustible
    @property
    def get_cons(self):
        if self.potencia:
            return round(self.potencia * self.budget.ratio_consumo_equipos, 1)
        return 0

    @property
    def get_costo_combustible(self):
        return round(self.get_precio_combustible * self.get_cons, 2)

    @property
    def get_lubricante(self):
        return round(self.get_costo_combustible * self.budget.ratio_lubricante / 100, 2)

    @property
    def get_cost_unit(self):
        ratio = self.budget.ratio_equipment
        exchange = self.budget.exchange_rate
        currency = self.budget.currency

        cost = self.get_costo_apu_hs_alq + self.get_lubricante
        
        if self.budget.is_cliente_asume_combustible == False:
            cost = cost + self.get_costo_combustible

        if currency == "D" and self.currency == "S":
            cost = cost / exchange
        elif currency == "S" and self.currency == "D":
            cost = cost * exchange

        return cost

    @property
    def get_quantity(self):
        quantity = 0
        for item in self.equipments_budget_equipment_task.all():
            quantity += item.quantity
        return quantity

    @property
    def get_standby_hours(self):
        quantity = 0
        for item in self.equipments_budget_equipment_task.all():
            quantity += round(
                item.task.quantity *
                item.get_efficiency * item.quantity, 2)
        return quantity

    @property
    def get_standby_estimated_hours(self):
        return (
            self.quantity *
            self.time_valorize *
            self.budget.workdays_per_month *
            self.hours_equipment_operation
        )

    @property
    def get_standby_cost(self):
        delta = self.get_standby_estimated_hours - self.get_standby_hours
        if delta > 0:
            return delta * self.get_cost_unit
        return 0.0

    @property
    def get_resource_name(self):
        return self.equipment.name

    @property
    def get_resource_code(self):
        return self.equipment.code

    @property
    def get_resource_label(self):
        return "{0} - {1} ({2})".format(
            self.equipment.code,
            self.equipment.name,
            self.equipment.unit)

    @property
    def get_resource_id(self):
        return self.equipment.id


class ResourceTaskBase(FollowUserModel):
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    efficiency = models.DecimalField(
        'rendimiento',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=1
    )
    position = models.PositiveIntegerField(
        'posición',
        blank=False,
        null=False,
        default=0
    )

    class Meta:
        abstract = True


@reversion.register()
class ManpowerTask(ResourceTaskBase):
    """
    Analisis de precios de la mano de obra de una tarea
    """
    task = models.ForeignKey(
        "TaskBudget",
        verbose_name="tarea",
        related_name="tasks_manpower_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    manpower = models.ForeignKey(
        Manpower,
        verbose_name="mano de obra",
        related_name="manpowers_manpower_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    manpower_budget = models.ForeignKey(
        ManpowerBudget,
        related_name="manpowers_budget_manpower_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):              # __unicode__ on Python 2
        code = self.task.budget.code
        return "{0} - {1}".format(code, self.manpower.name)

    class Meta:
        verbose_name = "mano de obra por tarea"
        verbose_name_plural = "manos de obra por tarea"

    @property
    def get_efficiency(self):
        if self.task.get_efficiency:
            return round(Decimal('8.00') / self.task.get_efficiency, 6)
        else:
            return 1.00

    # @property
    # def get_factor(self):
    #     return round(Decimal(str(self.rendimiento)) * self.quantity, 6)

    @property
    def get_subtotal(self):
        return round(
            Decimal(str(self.get_resource_price)) *
            Decimal(str(self.get_efficiency)) *
            Decimal(str(self.quantity)), 2)

    @property
    def get_manpower_name(self):
        return "{0} {1} ({2})".format(
            self.manpower.code or "",
            self.manpower.name,
            self.manpower.unit
        )

    @property
    def get_resource_label(self):
        return "{0} {1} ({2})".format(
            self.manpower.code or "",
            self.manpower.name,
            self.manpower.unit
        )

    @property
    def get_task_name(self):
        return self.task.name

    @property
    def get_resource_price(self):
        price = self.manpower_budget.get_cost_unit
        return price


@reversion.register()
class MaterialTask(ResourceTaskBase):
    """
    Analisis de precios del material de una tarea
    """
    task = models.ForeignKey(
        "TaskBudget",
        verbose_name="tarea",
        related_name="tasks_material_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material,
        verbose_name="material",
        related_name="materials_material_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    material_budget = models.ForeignKey(
        MaterialBudget,
        related_name="materials_budget_material_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):              # __unicode__ on Python 2
        return self.material.name

    class Meta:
        verbose_name = "material por tarea"
        verbose_name_plural = "materiales por tarea"

    @property
    def get_efficiency(self):
        return self.efficiency

    @property
    def get_resource_label(self):
        return "{0} {1} ({2})".format(
            self.material.code or "",
            self.material.name,
            self.material.unit
        )

    @property
    def get_task_name(self):
        return self.task.name

    @property
    def get_subtotal(self):
        return round(
            Decimal(str(self.get_resource_price)) *
            Decimal(str(self.get_efficiency)) *
            Decimal(str(self.quantity)), 2)

    @property
    def get_resource_price(self):
        price = self.material_budget.get_cost_unit
        return price


@reversion.register()
class SubcontractTask(ResourceTaskBase):
    """
    Analisis de precios del subcontrato de una tarea
    """
    task = models.ForeignKey(
        "TaskBudget",
        verbose_name="tarea",
        related_name="tasks_subcontract_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    subcontract = models.ForeignKey(
        Subcontract,
        verbose_name="subcontract",
        related_name="subcontracts_subcontract_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    subcontract_budget = models.ForeignKey(
        SubcontractBudget,
        related_name="subcontracts_budget_subcontract_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):              # __unicode__ on Python 2
        return self.subcontract.name

    class Meta:
        verbose_name = "subcontrato por tarea"
        verbose_name_plural = "subcontratos por tarea"

    @property
    def get_efficiency(self):
        return self.efficiency

    @property
    def get_resource_label(self):
        return "{0} {1} ({2})".format(
            self.subcontract.code or "",
            self.subcontract.name,
            self.subcontract.unit
        )

    @property
    def get_task_name(self):
        return self.task.name

    @property
    def get_subtotal(self):
        return round(
            Decimal(str(self.get_resource_price)) *
            Decimal(str(self.get_efficiency)) *
            Decimal(str(self.quantity)), 2)

    @property
    def get_resource_price(self):
        price = self.subcontract_budget.get_cost_unit
        return price


@reversion.register()
class EquipmentTask(ResourceTaskBase):
    """
    Analisis de equipos de una tarea
    """
    task = models.ForeignKey(
        "TaskBudget",
        verbose_name="tarea",
        related_name="tasks_equipment_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        Equipment,
        verbose_name="equipment",
        related_name="equipments_equipment_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    equipment_budget = models.ForeignKey(
        EquipmentBudget,
        related_name="equipments_budget_equipment_task",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):              # __unicode__ on Python 2
        return self.equipment.name

    class Meta:
        verbose_name = "equipo por tarea"
        verbose_name_plural = "equipos por tarea"

    @property
    def get_efficiency(self):
        if self.task.get_efficiency:
            return round(Decimal('8.00') / self.task.get_efficiency, 6)
        else:
            return 1.00

    @property
    def get_resource_label(self):
        return "{0} {1} ({2})".format(
            self.equipment.code or "",
            self.equipment.name,
            self.equipment.unit
        )

    @property
    def get_task_name(self):
        return self.task.name

    @property
    def get_subtotal(self):
        return round(
            Decimal(str(self.get_resource_price)) *
            Decimal(str(self.get_efficiency)) *
            Decimal(str(self.quantity)), 2)

    @property
    def get_resource_price(self):
        price = self.equipment_budget.get_cost_unit
        return price


@reversion.register()
class MemberBudget(FollowUserModel):
    """
    Los usuarios que serán miembros de un presupuesto
    """
    user = models.ForeignKey(
        User,
        verbose_name="miembro",
        related_name="users_member_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    budget = models.ForeignKey(
        "Budget",
        verbose_name="presupuesto",
        related_name="members_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)


@reversion.register()
class EPPBudget(FollowUserModel):
    """
    Presupuesto EPP
    """
    budget = models.ForeignKey(
        Budget,
        verbose_name="presupuesto",
        related_name="epps_budget",
        on_delete=models.CASCADE
    )
    tipo_epp = models.ForeignKey(
        GruposVarios,
        verbose_name="tipo de epp",
        related_name="tipo_epps_grupo",
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        limit_choices_to={'grupo': constants.GRUPO_TIPO_EPP}
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.pk, self.budget)

    class Meta:
        ordering = ("id",)
        unique_together = (("budget", "tipo_epp"))

    @property
    def get_tipo_epp_display(self):
        return self.tipo_epp.nombre

    @property
    def get_costo(self):
        suma_acumulada = Decimal("0.00")
        for item in self.detail_epps_budget.all():
            suma_acumulada += item.get_parcial
        if self.budget.currency == "D":
            suma_acumulada = suma_acumulada * self.budget.exchange_rate
        return suma_acumulada

    @property
    def get_costo_mes(self):
        if self.budget.meses_epp == 0:
            return 0
        return self.get_costo / self.budget.meses_epp


@reversion.register()
class EPPBudgetDetail(FollowUserModel):
    """
    Detalle de presupuesto EPP
    """
    epp_budget = models.ForeignKey(
        EPPBudget,
        verbose_name="prepuesto de epp",
        related_name="detail_epps_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        MaterialBudget,
        verbose_name="epp material",
        related_name="material_epps_budget",
        blank=True, # cambiar a False si es necesario
        null=True, # cambiar a False si es necesario
        on_delete=models.CASCADE,
    )
    unidad = models.CharField(
        'unidad',
        max_length=12,
        blank=False,
        null=False,
    )
    periodo_reposicion = models.DecimalField(
        verbose_name='periodo de reposicion',
        max_digits=5, decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=1
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.epp_budget, self.material)

    class Meta:
        ordering = ("id",)
        unique_together = (("epp_budget", "material"))

    @property
    def get_demanda(self):
        if self.periodo_reposicion == 0:
            return 0
        return math.ceil(self.epp_budget.budget.meses_epp / self.periodo_reposicion)

    @property
    def get_parcial(self):
        return self.material.get_cost_unit * self.quantity * self.get_demanda

    @property
    def get_material_display(self):
        return self.material.material.name