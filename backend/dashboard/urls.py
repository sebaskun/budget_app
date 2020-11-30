# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from django.conf.urls import url
from . import views

app_name = "dashboard"

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
]
