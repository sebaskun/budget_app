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
    Manpower,
    Material,
    Subcontract,
    Equipment
)


# from dal import autocomplete

# import datetime

# from .utils import build_budget_xml
# from . import errors

app_name = "resource"


@method_decorator(login_required, name='dispatch')
class ResourceView(TemplateView):
    template_name = "resource/resource.html"

    def get_context_data(self, **kwargs):
        context = super(ResourceView, self).get_context_data(**kwargs)
        # budgets = Budget.objects.all()

        # context['budgets'] = budgets

        return context


# @method_decorator(login_required, name='dispatch')
# class ManpowerResourceView(TemplateView):
#     template_name = "resource/manpower.html"

#     def get_context_data(self, **kwargs):
#         context = super(ManpowerResourceView, self).get_context_data(**kwargs)
#         # budgets = Budget.objects.all()

#         # context['budgets'] = budgets
#         return context


@method_decorator(login_required, name='dispatch')
class MaterialResourceView(TemplateView):
    template_name = "resource/resource_base.html"

    def get_context_data(self, **kwargs):
        context = super(MaterialResourceView, self).get_context_data(**kwargs)
        # budgets = Budget.objects.all()

        context['title'] = "Recursos: Materiales"
        context['add_button_text'] = "Adicionar Materialxx"
        context['category_url'] = "/resource/api/category_material/"
        context['filter_data'] = "categorias"
        context['filter_name'] = "name"
        context['filter_count'] = "get_count"
        context['filter_text'] = "Materiales categorizados"
        context['grid_fields'] = ['code', 'name', 'unit', 'cost']
        context['grid_fields_title'] = ['Cód.', 'Nombre', 'Unidad', 'Precio']
        context['grid_fields_right_align'] = ['cost']
        context['add_filter_text'] = "Crear nueva Categoria"
        context['search_placeholder'] = "Buscar material"
        context['data_url'] = "/resource/api/material/"
        context['category_url'] = "/resource/api/category_material/"
        return context

@method_decorator(login_required, name='dispatch')
class SubcontractResourceView(TemplateView):
    template_name = "resource/resource_base.html"

    def get_context_data(self, **kwargs):
        context = super(SubcontractResourceView, self).get_context_data(**kwargs)
        # budgets = Budget.objects.all()

        context['title'] = "Recursos: Subcontratos"
        context['add_button_text'] = "Adicionar Subcontrato"
        context['filter_data'] = "categorias"
        context['filter_name'] = "name"
        context['filter_count'] = "get_count"
        context['filter_text'] = "Materiales categorizados"
        context['grid_fields'] = ['code', 'name', 'unit', 'cost']
        context['grid_fields_title'] = ['Cód.', 'Nombre', 'Unidad', 'Precio']
        context['grid_fields_right_align'] = ['cost']
        context['add_filter_text'] = "Crear nueva Categoria"
        context['search_placeholder'] = "Buscar material"
        context['data_url'] = "/resource/api/material/"
        context['category_url'] = "/resource/api/category_material/"
        return context


@method_decorator(login_required, name='dispatch')
class ManpowerResourceView(TemplateView):
    template_name = "resource/resource_base.html"

    def get_context_data(self, **kwargs):
        context = super(ManpowerResourceView, self).get_context_data(**kwargs)
        # budgets = Budget.objects.all()

        context['title'] = "Recursos: Mano de Obra"
        context['add_button_text'] = "Adicionar Mano de obra"
        context['data_url'] = "/resource/api/manpower/"
        context['category_url'] = "/resource/api/category_manpower/"
        context['filter_data'] = "categorias"
        context['filter_name'] = "name"
        context['filter_count'] = "get_count"
        context['filter_text'] = "Mano de obra categorizados"
        context['grid_fields'] = ['code', 'name', 'unit', 'cost']
        context['grid_fields_title'] = ['Cód.', 'Nombre', 'Unidad', 'Precio']
        context['grid_fields_right_align'] = ['cost']
        context['add_filter_text'] = "Crear nueva Categoria"
        context['search_placeholder'] = "Buscar mano de obra"
        return context


@method_decorator(login_required, name='dispatch')
class EquipmentResourceView(TemplateView):
    template_name = "resource/resource_base.html"

    def get_context_data(self, **kwargs):
        context = super(EquipmentResourceView, self).get_context_data(**kwargs)
        # budgets = Budget.objects.all()

        context['title'] = "Recursos: Equipo"
        context['add_button_text'] = "Adicionar Equipo"
        context['data_url'] = "/resource/api/equipment/"
        context['category_url'] = "/resource/api/category_equipment/"
        context['filter_data'] = "categorias"
        context['filter_name'] = "name"
        context['filter_count'] = "get_count"
        context['filter_text'] = "Equipos categorizados"
        context['grid_fields'] = ['code', 'name', 'unit', 'cost']
        context['grid_fields_title'] = ['Cód.', 'Nombre', 'Unidad', 'Precio']
        context['grid_fields_right_align'] = ['cost']
        context['add_filter_text'] = "Crear nueva Categoria"
        context['search_placeholder'] = "Buscar equipo"
        return context

