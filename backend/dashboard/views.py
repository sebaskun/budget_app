# coding=utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponse

from ..budget.models import Budget


# from dal import autocomplete

# import datetime

# from .utils import build_budget_xml
# from . import errors


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard"
        context['budgets'] = Budget.objects.all()[:5]
        return context
