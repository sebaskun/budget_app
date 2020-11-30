# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from ..core import constants
from ..core.utils import CharNullField
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError

site = "http://localhost:8000"


class Client(models.Model):
    name = CharNullField(
        'nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    short_name = CharNullField(
        'nombre corto',
        max_length=40,
        blank=True,
        null=True,
    )
    initials = CharNullField(
        'iniciales',
        max_length=3,
        blank=False,
        null=False,
    )
    ruc = CharNullField(
        'RUC',
        max_length=11,
        blank=True,
        null=True,
    )
    address = models.CharField(
        'dirección',
        max_length=150,
        blank=True,
        null=True,
    )
    logo = models.ImageField(
        upload_to="client",
        verbose_name='logo',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.get_short_name

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        permissions = (
            ("can_add_client", "Puede adicionar cliente"),
            ("can_edit_client", "Puede modificar cliente"),
            ("can_change_status_client", "Puede cambiar estado cliente"),
            ("can_see_view_client", "Puede ver cliente"),
        )

    @property
    def get_short_name(self):
        return self.short_name or self.name[:30] + \
                "..." if len(self.name) > 30 else self.name

    @property
    def get_image_small(self):
        if self.logo:
            try:
                return site + get_thumbnailer(self.logo)['small'].url
            except InvalidImageFormatError:
                return ""

    @property
    def get_image_medium(self):
        if self.logo:
            try:
                return site + get_thumbnailer(self.logo)['medium'].url
            except InvalidImageFormatError:
                return ""

    @property
    def get_image_medium_h(self):
        if self.logo:
            try:
                return site + get_thumbnailer(self.logo)['medium_h'].url
            except InvalidImageFormatError:
                return ""

    @property
    def get_image_large(self):
        if self.logo:
            try:
                return site + get_thumbnailer(self.logo)['large'].url
            except InvalidImageFormatError:
                return ""

    @property
    def get_image_miniature_50_0(self):
        if self.logo:
            try:
                return site + get_thumbnailer(self.logo)['miniature_50_0'].url
            except InvalidImageFormatError:
                return ""

class Contact(models.Model):
    cliente = models.ForeignKey(
        Client,
        verbose_name="cliente",
        related_name="clients_contact",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(
        'nombre',
        max_length=128,
        blank=False,
        null=False,
    )
    cargo = models.CharField(
        'cargo',
        max_length=35,
        blank=True,
        null=True,
    )
    observacion = models.CharField(
        'observación',
        max_length=100,
        blank=True,
        null=True,
    )
    position = models.PositiveIntegerField()

    def __unicode__(self):              # __unicode__ on Python 2
        return self.nombre

    class Meta:
        verbose_name = "contacto"
        verbose_name_plural = "contactos"


class MeansContact(models.Model):
    """
    Medio de contacto
    """
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )
    tipo = models.IntegerField(
        'tipo',
        blank=False,
        null=False,
        choices=constants.MEDIOS_CONTACTO,
        default=constants.MEDIOS_CONTACTO_DEFAULT
    )
    dato = models.CharField(
        'dato',
        max_length=35,
        blank=False,
        null=False,
    )
    observacion = models.CharField(
        'observación',
        max_length=100,
        blank=True,
        null=True,
    )
    # default = models.BooleanField(
    #     '¿por defecto?',
    #     default=True
    # )
    position = models.PositiveIntegerField()

    def __unicode__(self):              # __unicode__ on Python 2
        return self.dato

    class Meta:
        verbose_name = "medio de contacto"
        verbose_name_plural = "medios de contacto"

