# coding=utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
# from django.core.urlresolvers import get_script_prefix
from django.shortcuts import redirect
# from utils import next_url


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['current_page'] = 'home'

        return context
