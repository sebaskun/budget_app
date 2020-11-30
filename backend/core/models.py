# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from . import constants

import reversion
from django_extensions.db.models import TimeStampedModel
from .middleware import local
from django.conf import settings

NULL_AND_BLANK = {'null': True, 'blank': True}


class FollowUserModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        **NULL_AND_BLANK)
    modified = models.DateTimeField(
        auto_now=True,
        **NULL_AND_BLANK)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        **NULL_AND_BLANK,
        editable=False,
        related_name='%(class)s_created',
        on_delete=models.CASCADE)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        **NULL_AND_BLANK,
        editable=False,
        related_name='%(class)s_modified',
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        user = local.user
        self.modified_by = user
        if self.pk is None and hasattr(local, 'user'):
            self.created_by = user
        return super(FollowUserModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Correlative(models.Model):
    """
    Almacena los correlativos de los documentos
    """
    model = models.CharField(
        verbose_name="modelo",
        choices=constants.MODELOS,
        max_length=3,
    )
    prefix = models.CharField(
        verbose_name="prefijo",
        max_length=10,
        blank=True,
        null=True
    )
    current_number = models.IntegerField(
        verbose_name="número actual",
        default=0
    )

    # def get_correlative(self, model, prefix, ceros=3):
    #     current, new = Correlative.objects.get_or_create(model=model,
    #                                                      prefix=prefix,
    #                                                      defaults={'current_number': 0})
    #     correlative = current.current_number + 1
    #     prefix = current.prefix if current.prefix else ""
    #     new_correlative = u"%s" % (str(correlative).zfill(ceros))
    #     current.current_number = correlative
    #     current.save()
    #     return new_correlative

    def __unicode__(self):              # __unicode__ on Python 2
        return "{} {}".format(self.prefix, self.current_number)

    class Meta:
        verbose_name = "correlativo"
        verbose_name_plural = "correlativos"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_(u'dirección de correo'),
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='nombres',
        max_length=50,
        null=True,
        blank=True,
    )
    lastname = models.CharField(
        verbose_name='apellidos',
        max_length=50,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(
        verbose_name='Foto',
        upload_to="image_user",
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def get_full_name(self):
        # The user is identified by their email address
        full_name = "{} {}".format(self.name or '', self.lastname or '')
        return full_name if full_name.strip() else ''

    def get_short_name(self):
        name = "(Sin Nombre)"
        if self.name is not None:
            name = self.name
        return name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = _(u"Usuario")
        verbose_name_plural = _(u"Usuarios")

    # def __unicode__(self):
    #     return unicode(self.name)


@reversion.register()
class GruposVarios(TimeStampedModel, models.Model):
    """
    Listas Grupos Varios del sistema
    """
    nombre = models.CharField(
        'nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    grupo = models.CharField(
        'grupo',
        max_length=3,
        blank=False,
        null=False,
        choices=constants.GRUPOS_VARIOS
    )
    activo = models.BooleanField(default=True)
    predeterminado = models.BooleanField(default=False)

    def __str__(self):
        return "{}-{}".format(self.grupo, self.nombre)

    class Meta:
        verbose_name = _(u"grupo varios")
        verbose_name_plural = _(u"grupos varios")
        ordering = ("grupo", "nombre")

    @property
    def get_grupo_nombre(self):
        return self.get_grupo_display


@reversion.register()
class Regimen(TimeStampedModel, models.Model):
    """
    Listas Regimen del sistema
    """
    regimen = models.ForeignKey(
        GruposVarios,
        verbose_name=u'regimen',
        related_name="grupos_regimen",
        on_delete=models.CASCADE,
        limit_choices_to={
            'grupo': constants.GRUPO_REGIMEN,
            'activo': True}
    )
    sueldo = models.DecimalField(
        'sueldo',
        max_digits=8, decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    currency = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    categoria_trabajador = models.ForeignKey(
        GruposVarios,
        verbose_name=u'categoria',
        related_name="categorias_regimen",
        on_delete=models.CASCADE,
        limit_choices_to={
            'grupo': constants.GRUPO_CATEGORIA_TRABAJADOR,
            'activo': True}
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = _(u"regimen")
        verbose_name_plural = _(u"regimenes")
        ordering = ("regimen", "categoria_trabajador",)
        unique_together = ("regimen", "categoria_trabajador")

    # @property
    # def get_tipo_nombre(self):
    #     return self.get_tipo_display

    @property
    def get_categoria_trabajador_nombre(self):
        return self.categoria_trabajador.nombre

    @property
    def get_regimen_nombre(self):
        return self.regimen.nombre

    def __str__(self):
        return "{}-{}".format(self.regimen.nombre, self.categoria_trabajador.nombre)


@reversion.register()
class Certificado(TimeStampedModel, models.Model):
    """
    Listado de Costo de Certificaciones
    """
    nombre = models.CharField(
        'nombre',
        max_length=150,
        blank=False,
        null=False
    )
    importe = models.DecimalField(
        'importe',
        max_digits=8, decimal_places=2,
        blank=False,
        null=False,
        default=0
    )
    currency = models.CharField(
        'moneda',
        max_length=1,
        blank=False,
        null=False,
        choices=constants.MONEDAS,
        default=constants.MONEDAS_DEFAULT
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "certificado"
        verbose_name_plural = "certificados"
        ordering = ("nombre",)

    def __str__(self):
        return self.nombre