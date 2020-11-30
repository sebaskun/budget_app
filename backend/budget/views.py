# coding=utf-8
from __future__ import unicode_literals

from copy import copy

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponse

from .models import Budget, TaskBudget


# from dal import autocomplete

import datetime

from .utils import build_budget_xml
from . import errors


def copy_budget(budget):
    """
    Función para copiar un presupuesto y sus recursos y tareas
    Creado: 10 feb de 2019
    Por: Carlos Maldonado
    """
    pass


def copy_task(task):
    """
    Función para copiar una tarea y sus recursos
    Creado: 10 feb de 2019
    Por: Carlos Maldonado
    """
    new_task = copy(task)
    new_task.id = None
    new_task.name = "Copia - {}".format(new_task.name)
    new_task.save()
    recursos = [
        'tasks_manpower_task',
        'tasks_material_task',
        'tasks_subcontract_task',
        'tasks_equipment_task']
    for recurso in recursos:
        instancia = getattr(task, recurso)
        for item in instancia.all():
            item.id = None
            item.task_id = new_task.id
            item.save()
    return new_task

@method_decorator(login_required, name='dispatch')
class BudgetView(TemplateView):
    template_name = "budget/budget.html"

    def get_context_data(self, **kwargs):
        context = super(BudgetView, self).get_context_data(**kwargs)
        budgets = Budget.objects.all()
        # osm_moved = OsmMoved.objects.all().order_by("-created")[:5]
        # form_entry = FormEntry.objects.filter(osm__isnull=False).order_by("-modified")[:5]
        # osm_files = OsmImage.objects.filter(osm__isnull=False).order_by("-modified")[:5]
        # can_see = "%s.can_see_location" % Osm._meta.app_label
        # can_see_location = self.request.user.has_perm(can_see)
        # # import pdb; pdb.set_trace()
        context['current_page'] = 'presupuesto'
        context['title'] = "Presupuesto"
        context['budgets'] = budgets
        # context['can_see_location'] = can_see_location

        # can_see = "%s.can_see_jr" % JobRequest._meta.app_label
        # can_see_jr = self.request.user.has_perm(can_see)
        # can_see = "%s.can_see_wo" % WorkOrder._meta.app_label
        # can_see_wo = self.request.user.has_perm(can_see)
        # can_see = "%s.can_see_wo_valued" % WorkOrder._meta.app_label
        # can_see_wo_valued = self.request.user.has_perm(can_see)

        # context['current_page'] = 'budget_view'
        # context['can_see_jr'] = can_see_jr
        # context['can_see_wo'] = can_see_wo
        # context["can_see_wo_valued"] = can_see_wo_valued

        return context


@method_decorator(login_required, name='dispatch')
class APUView(TemplateView):
    template_name = "budget/apu_task_budget.html"

    def get_context_data(self, **kwargs):
        context = super(APUView, self).get_context_data(**kwargs)
        # budget = Budget.objects.get(pk=kwargs['pk_budget'])
        task = TaskBudget.objects.get(pk=kwargs['pk_task'])
        # tasks = TaskBudget.objects.filter(presupuesto_id=budget.pk)
        # context['budget'] = budget
        context['task'] = task

        return context


@method_decorator(login_required, name='dispatch')
class BudgetTasksView(TemplateView):
    template_name = "budget/budget_tasks.html"

    def get_context_data(self, **kwargs):
        context = super(BudgetTasksView, self).get_context_data(**kwargs)
        show_calendar = self.request.GET.get('calendar') or ""
        budget = Budget.objects.get(pk=kwargs['pk'])
        context['budget'] = budget
        context['show_calendar'] = show_calendar
        return context


@method_decorator(login_required, name='dispatch')
class ImportTaskView(TemplateView):
    template_name = "admin/budget/change_list.html"

    def get_context_data(self, **kwargs):
        context = super(ImportTaskView, self).get_context_data(**kwargs)
        context['current_page'] = 'budget_view'
        return context


@method_decorator(login_required, name='dispatch')
class APUEditView(TemplateView):
    template_name = "admin/budget/change_form.html"

    def get_context_data(self, **kwargs):
        context = super(APUEditView, self).get_context_data(**kwargs)
        context['current_page'] = 'budget_view'
        return context

@login_required
def export_budget_xml(request, pk):
    # budget = self.get_object(request, budget_id)
    root = build_budget_xml(pk)
    file_name = "{}-{}".format(
        Budget.objects.get(id=pk).code,
        datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    response = HttpResponse(root, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s.xml' % (file_name,)
    return response
