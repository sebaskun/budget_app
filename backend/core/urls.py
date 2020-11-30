# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

# from . import views
from .api import (
    UserViewSet,
    GruposVariosViewSet,
    RegimenViewSet,
    CertificadoViewSet
)
from .views import HomeView


app_name = "core"

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'grupos_varios', GruposVariosViewSet)
router.register(r'regimen', RegimenViewSet)
router.register(r'certificado', CertificadoViewSet)


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^api/', include(router.urls)),
]

