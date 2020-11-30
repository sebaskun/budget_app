# coding=utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponse

from .models import (
    Client,
)


# from dal import autocomplete

# import datetime

# from .utils import build_budget_xml
# from . import errors

app_name = "client"


@method_decorator(login_required, name='dispatch')
class ClientView(TemplateView):
    template_name = "client/client.html"

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        # budgets = Budget.objects.all()

        context['title'] = "Clientes"
        context['add_button_text'] = "Adicionar Cliente"
        context['data_url'] = "/client/api/clients/"
        # context['category_url'] = "/resource/api/category_manpower/"
        # context['filter_data'] = "categorias"
        # context['filter_name'] = "name"
        # context['filter_count'] = "get_count"
        # context['filter_text'] = "Mano de obra categorizados"
        context['grid_fields'] = ['initials', 'short_name', 'ruc']
        context['grid_fields_title'] = ['Cód.', 'Nombre', 'ruc']
        # context['grid_fields_right_align'] = ['cost']
        # context['add_filter_text'] = "Crear nueva Categoria"
        context['search_placeholder'] = "Buscar cliente"
        return context
