# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
import reversion

from ..core import constants
from ..core.utils import CharNullField
from ..core.models import GruposVarios

from backend.core.models import FollowUserModel

class ResourceBase(FollowUserModel):
    """
    Abstracción para los recursos
    """
    code = CharNullField(
        verbose_name='código',
        max_length=30,
        blank=True,
        null=True,
        unique=True
    )
    name = models.CharField(
        verbose_name='nombre',
        max_length=200,
        blank=False,
        null=False
    )
    description = models.TextField(
        'descripción',
        blank=True,
        null=True
    )
    unit = models.CharField(
        verbose_name='unidad de costo',
        max_length=15,
        blank=True,
        null=True,
    )
    currency = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.CURRENCIES,
        default=constants.CURRENCIES_DEFAULT
    )
    cost = models.DecimalField(
        'costo unitario',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    pull_in_new_budget = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CategoryBase(FollowUserModel):
    name = models.CharField(
        verbose_name='nombre',
        max_length=150,
        blank=False,
        null=False
    )

    description = models.TextField(
        verbose_name='descripción',
        blank=True,
        null=True
    )

    image = models.ImageField(
        'imagen',
        upload_to="image_category",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


@reversion.register()
class Manpower(ResourceBase):
    """
    Mano de obra
    """

    # category = models.ForeignKey(
    #     "CategoryManpower",
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE
    # )
    # business_cost = models.DecimalField(
    #     'costo empresarial',
    #     max_digits=15, decimal_places=6,
    #     blank=False,
    #     null=False,
    #     default=0
    # )
    sueldo_bruto = models.DecimalField(
        'sueldo bruto',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=0
    )
    # epp_cost = models.DecimalField(
    #     'costo epp',
    #     max_digits=15, decimal_places=6,
    #     blank=False,
    #     null=False,
    #     default=0
    # )
    type_cost = models.CharField(
        'tipo de costo',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.TYPE_COST,
        default=constants.TYPE_COST_DEFAULT
    )
    allows_ratio = models.PositiveIntegerField(
        'Permite coeficiente?',
        blank=False,
        null=False,
        default=1
    )
    tipo_regimen = models.CharField(
        'tipo de regimen',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.TIPOS_REGIMEN,
        default=constants.TIPOS_REGIMEN_DEFAULT
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mano de obra"
        verbose_name_plural = "manos de obra"
        ordering = ('code', 'name')

    @property
    def get_type_cost_display2(self):
        """
        Tipo de costo
        """
        if self.type_cost:
            return self.get_type_cost_display()
        return None

    @property
    def get_tipo_regimen_display2(self):
        """
        Tipo de costo
        """
        if self.tipo_regimen:
            return self.get_tipo_regimen_display()
        return None


@reversion.register()
class Material(ResourceBase):
    """
    Material
    """
    category = models.ForeignKey(
        "CategoryMaterial",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="material",
        verbose_name='image',
        blank=True,
        null=True
    )
    class_cost = models.CharField(
        'clase de costo',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.TYPE_MATERIAL,
        default=constants.TYPE_MATERIAL_DEFAULT
    )
    is_subcontract = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    

    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"
        ordering = ['name', 'code']


@reversion.register()
class Subcontract(ResourceBase):
    """
    Subcontrato
    """
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "subcontrato"
        verbose_name_plural = "subcontratos"
        ordering = ['name', 'code']

# @reversion.register()
# class OverHead(ResourceBase):
#     """
#     Gastos Generales
#     """
#     class_cost = models.CharField(
#         'clase de costo',
#         max_length=1,
#         blank=False,
#         null=False,
#         choices=constants.CLASS_OVERHEAD,
#         default=constants.CLASS_OVERHEAD_DEFAULT
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "gasto general"
#         verbose_name_plural = "gastos generales"

@reversion.register()
class Equipment(ResourceBase):
    """
    Equipo
    """
    hours_equipment_operation = models.DecimalField(
        'horas de operación del equipo',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,
        default=8
    )
    category = models.ForeignKey(
        "CategoryEquipment",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    potencia = models.DecimalField(
        'potencia del equipo',
        max_digits=6, decimal_places=2,
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to="equipment",
        verbose_name='image',
        blank=True,
        null=True
    )
    has_combustible = models.BooleanField(default=False)
    tipo_combustible = models.CharField(
        'tipo de combustible',
        max_length=2,
        blank=True,
        null=True,
        choices=constants.COMBUSTIBLE,
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "equipo"
        verbose_name_plural = "equipos"

    @property
    def get_category_display(self):
        if self.category:
            return self.category.name
        return None

class CategoryManpower(CategoryBase):

    class Meta:
        verbose_name = "categoría de mano de obra"
        verbose_name_plural = "categorías de mano de obra"
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def get_count(self):
        return len(self.manpower_set.all())


class CategoryMaterial(CategoryBase):

    class Meta:
        verbose_name = "categoría de material"
        verbose_name_plural = "categorías de materiales"

    def __str__(self):
        return self.name

    @property
    def get_count(self):
        return len(self.material_set.all())


class CategoryEquipment(CategoryBase):

    padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='category_padre',
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = "categoría de equipo"
        verbose_name_plural = "categorías de equipos"
        ordering = ('name',)

    def __str__(self):
        if self.padre:
            return "{}: {}".format(self.padre.name, self.name)
        return self.name

    @property
    def get_count(self):
        return len(self.equipment_set.all())


@reversion.register()
class Vacuna(FollowUserModel):
    """
    Vacuna
    """
    nombre = models.CharField(
        verbose_name="nombre",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )
    ubicacion = models.ForeignKey(
        GruposVarios,
        verbose_name="ubicacion",
        related_name="ubicaciones_vacuna",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'grupo': constants.GRUPO_UBICACION}
    )
    moneda = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.CURRENCIES,
        default=constants.CURRENCIES_DEFAULT
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    @property
    def get_costo_vacuna(self):
        suma_acumulada = 0
        for item in self.details_vacuna.all():
            suma_acumulada += item.get_precio_parcial
        return suma_acumulada

    @property
    def get_ubicacion_display(self):
        return self.ubicacion.nombre

@reversion.register()
class VacunaDetail(FollowUserModel):
    """
    Detalle del Presupuesto de Vacunas
    """
    vacuna = models.ForeignKey(
        Vacuna,
        verbose_name="Vacuna",
        related_name="details_vacuna",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    material = models.ForeignKey(
        Material,
        verbose_name="vacunas material",
        related_name="material_vacunas_budget",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    quantity = models.DecimalField(
        'cantidad',
        max_digits=15, decimal_places=6,
        blank=False,
        null=False,  
        default=1
    )
    observacion = models.TextField(
        'observacion',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ("material",)
        unique_together = (("vacuna", "material"))

    def __str__(self):
        return "{} {}".format(self.vacuna, self.material)

    @property
    def get_precio_parcial(self):
        return self.material.cost * self.quantity
    
    @property
    def get_material_display(self):
        return self.material.name

    @property
    def get_material_moneda(self):
        return self.material.currency