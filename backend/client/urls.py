# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from django.conf.urls import url
from . import views
from .api import (
    ClientViewSet
)

router = DefaultRouter()

router.register(r'clients', ClientViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.ClientView.as_view(), name="client"),
]
