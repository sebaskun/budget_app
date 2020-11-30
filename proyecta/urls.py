# coding=utf-8
from __future__ import unicode_literals
"""proyecta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.views.generic.base import RedirectView
from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.auth import get_user_model
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

# from rest_framework_extensions.routers import NestedRouterMixin
# from rest_framework_jwt.views import obtain_jwt_token

# from backend.budget import api
# from backend.client.api import (
#     ClientViewSet,
# )

# from backend.budget.api import (
#     ManpowerTaskViewSet,
#     TaskBudgetViewSet,
#     BudgetViewSet,
#     ManpowerBudgetListView,
#     ResourceBudgetViewSet,
#     StatusBudgetViewSet
# )

# from backend.resource.api import (
#     ManpowerViewSet,
#     MaterialViewSet,
#     EquipmentViewSet,
#     TypeManpowerViewSet,
#     TypeMaterialViewSet,
#     TypeEquipmentViewSet,
# )

favicon_view = RedirectView.as_view(url='/static/core/img/favicon.png', permanent=True)

# from django.contrib.auth import views as auth_views


admin.site.site_header = "PROYECTA"

User = get_user_model()


urlpatterns = [
    url(r'', include("backend.core.urls")),
    url(r'^dashboard', include("backend.dashboard.urls")),
    url(r'^budget/', include("backend.budget.urls")),
    url(r'^resource/', include("backend.resource.urls")),
    url(r'^client/', include("backend.client.urls")),
    # url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^admin/', admin.site.urls),
    # url(r'^nested_admin/', include('nested_admin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^static/(?P<path>.*)$',
            serve,
            {'document_root': '%s/static' % settings.BASE_DIR,
             'show_indexes': True}),
    ]

    # urlpatterns += [
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # ]
