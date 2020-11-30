# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# # from datetime import date
# # from copy import deepcopy

# from django.conf.urls import url
# from django.contrib import admin
# # from django.core.urlresolvers import reverse
# from django.urls import reverse

# from django.http import HttpResponseRedirect, HttpResponse
# from django.template.response import TemplateResponse
# from django_admin_row_actions import AdminRowActionsMixin
# from .utils import build_budget_xml

# import xml.etree.ElementTree as ET
# # from django import forms as _forms

# # from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

# from . import models
# from . import forms

# from ..core import utils, constants
# # from ..budget import models
# # from ..resource.forms import ManPowerBudgetModelForm

# from . import errors
# import nested_admin
# # from .forms import BudgetForm


# # class TaskInline(admin.TabularInline):
# #     model = models.Task
# # admin.site.disable_action('delete_selected')


# class ManpowerTaskBudgetInline(admin.TabularInline):
#     model = models.ManpowerTask
#     extra = 0

#     def get_formset(self, request, obj=None, **kwargs):
#         form = super(ManpowerTaskBudgetInline, self).get_formset(request, obj, **kwargs)
#         manpower_list = list(
#             obj.budget.manpowers_budget.all().values_list('manpower', flat=True)
#         )
#         form.form.base_fields['manpower'].queryset = \
#             models.Manpower.objects.filter(id__in=manpower_list)

#         return form


# class MaterialTaskBudgetInline(admin.TabularInline):
#     model = models.MaterialTask
#     extra = 0

#     def get_formset(self, request, obj=None, **kwargs):
#         form = super(MaterialTaskBudgetInline, self).get_formset(request,
#                                                                  obj,
#                                                                  **kwargs)
#         material_list = list(
#             obj.budget.materials_budget.all().values_list('material',
#                                                                  flat=True))
#         form.form.base_fields[
#             'material'].queryset = models.Material.objects.filter(
#             id__in=material_list)

#         return form


# class EquipmentTaskBudgetInline(admin.TabularInline):
#     model = models.EquipmentTask
#     extra = 0

#     def get_formset(self, request, obj=None, **kwargs):
#         form = super(
#             EquipmentTaskBudgetInline,
#             self).get_formset(request, obj, **kwargs)
#         equipment_list = list(
#             obj.budget.equipments_budget.all().values_list('equipo',
#                                                                  flat=True))
#         form.form.base_fields['equipment'].queryset = models.Equipment.objects.filter(
#             id__in=equipment_list)

#         return form


# class ManpowerBudgetInline(nested_admin.NestedTabularInline):
#     model = models.ManpowerBudget
#     form = forms.ManpowerBudgetModelForm
#     extra = 0
#     sortable_field_name = "position"
#     # show_change_link = True


# class MaterialBudgetInline(nested_admin.NestedTabularInline):
#     model = models.MaterialBudget
#     # form = ManPowerBudgetModelForm
#     extra = 0
#     sortable_field_name = "position"
#     # show_change_link = True


# class EquipmentBudgetInline(nested_admin.NestedTabularInline):
#     model = models.EquipmentBudget
#     # form = ManPowerBudgetModelForm
#     sortable_field_name = "position"
#     extra = 0
#     # show_change_link = True


# class TaskInline(nested_admin.NestedTabularInline):
#     model = models.TaskBudget
#     form = forms.TaskInlineForm
#     extra = 0
#     sortable_field_name = "position"
#     # show_change_link = True


# @admin.register(models.Budget)
# class BudgetAdmin(AdminRowActionsMixin, nested_admin.NestedModelAdmin):
#     """
#     """

#     form = forms.BudgetForm

#     list_display = [
#         'numero',
#         'proyecto',
#         'get_client',
#         'get_date_presentation',
#         'estado'
#     ]

#     list_filter = [
#         'proyecto__cliente',
#         'estado'
#     ]

#     search_fields = ['numero', 'proyecto__nombre', 'proyecto__cliente__nombre']

#     def get_urls(self):
#         urls = super(BudgetAdmin, self).get_urls()
#         custom_urls = [
#             url(
#                 r'^(?P<budget_id>.+)/import/$',
#                 self.admin_site.admin_view(self.process_import),
#                 name='budget-import-xml',
#             ),
#             url(
#                 r'^(?P<budget_id>.+)/export/$',
#                 self.admin_site.admin_view(self.process_export),
#                 name='budget-export-xml',
#             ),
#             # url(
#             #     r'^(?P<budget_id>.+)/export/$',
#             #     self.admin_site.admin_view(self.process_export_budget),
#             #     name='budget-export-xml',
#             # ),
#             # url(
#             #     r'^(?P<budget_id>.+)/apu/$',
#             #     self.admin_site.admin_view(self.process_apu_budget),
#             #     name='budget-apu',
#             # ),
#         ]
#         return custom_urls + urls

#     def process_import(self, request, budget_id, *args, **kwargs):
#         return self.process_action(
#             request=request,
#             budget_id=budget_id,
#             action_form=forms.ImportXMLForm,
#             action_title='Importar tareas desde XML',
#         )

#     def process_export(self, request, budget_id, *args, **kwargs):
#         # budget = self.get_object(request, budget_id)
#         root = build_budget_xml(budget_id)

#         response = HttpResponse(root, content_type='application/force-download')
#         response['Content-Disposition'] = 'attachment; filename=%s' % ("archivo.xml",)
#         return response

#     def process_action(
#         self,
#         request,
#         budget_id,
#         action_form,
#         action_title
#     ):
#         budget = self.get_object(request, budget_id)
#         if request.method != 'POST':
#             form = action_form()
#         else:
#             form = action_form(request.POST, request.FILES)
#             if form.is_valid():
#                 try:
#                     form.save(budget, request.user)
#                 except errors.Error as e:
#                     # If save() raised, the form will a have a non
#                     # field error containing an informative message.
#                     pass
#                 else:
#                     self.message_user(request, 'Success')
#                     url = reverse(
#                         'admin:budget_budget_change',
#                         args=[budget.pk],
#                         current_app=self.admin_site.name,
#                     )
#                     return HttpResponseRedirect(url)
#         context = self.admin_site.each_context(request)
#         context['opts'] = self.model._meta
#         context['form'] = form
#         context['budget'] = budget
#         context['title'] = action_title
#         return TemplateResponse(
#             request,
#             'admin/budget/budget_import_xml.html',
#             context,
#         )

#     def get_client(self, obj):
#         return obj.proyecto.cliente

#     get_client.short_description = 'cliente'
#     get_client.empty_value_display = '- -'
#     get_client.admin_order_field = 'proyecto__cliente'

#     def get_date_presentation(self, obj):
#         return obj.proyecto.fecha_presentacion_propuesta.strftime(utils.get_date_format(obj.proyecto.fecha_presentacion_propuesta))

#     get_date_presentation.short_description = 'fecha de presentación'
#     get_date_presentation.empty_value_display = '- -'
#     get_date_presentation.admin_order_field = 'proyecto__fecha_presentacion_propuesta'

#     inlines = [
#              ManpowerBudgetInline,
#              MaterialBudgetInline,
#              EquipmentBudgetInline,
#              # TaskInline,
#          ]

#     def get_row_actions(self, obj):
#         row_actions = [
#             {
#                 'label': 'Importar XML de tareas',
#                 'url': reverse('admin:budget-import-xml', args=[obj.pk]),
#                 'tooltip': 'Importa un archivo XML de las tareas',
#                 # 'enabled': obj.estado in [models.CHOICE_ESTADO_FACTURA_NUMERADO,
#                 #                           models.CHOICE_ESTADO_FACTURA_CERRADO],
#             },
#             {
#                 'label': 'Exportar XML de tareas',
#                 'url': reverse('admin:budget-export-xml', args=[obj.pk]),
#                 'tooltip': 'Exporta las tareas a un archivo XML',
#                 # 'enabled': obj.estado in [models.CHOICE_ESTADO_FACTURA_NUMERADO,
#                 #                           models.CHOICE_ESTADO_FACTURA_CERRADO],
#             },
#             # {
#             #     'label': 'APU de tareas',
#             #     'url': reverse('admin:apu_edit', kwargs={'pk': obj.pk}),
#             #     'tooltip': 'Permite ver y modificar APU por cada tarea',
#             #     # 'enabled': obj.estado in [models.CHOICE_ESTADO_FACTURA_NUMERADO,
#             #     #                           models.CHOICE_ESTADO_FACTURA_CERRADO],
#             # },
#             # {
#             #     'label': 'Exportar tareas y recursos',
#             #     'url': reverse('admin:budget-export-xml', kwargs={'pk': obj.pk}),
#             #     'tooltip': 'Exporta las tareas y recursos a un archivo XML',
#             #     # 'enabled': obj.estado in [models.CHOICE_ESTADO_FACTURA_NUMERADO,
#             #     #                           models.CHOICE_ESTADO_FACTURA_CERRADO],
#             # },
#         ]
#         row_actions += super(BudgetAdmin, self).get_row_actions(obj)
#         return row_actions

#     class Media:
#         js = (
#                 '/static/budget/js/manpower_budget.js',
#                 '/static/budget/js/material_budget.js',
#                 '/static/budget/js/equipment_budget.js',
#               )
#     # class Media:
#     #     css = {
#     #         'all': ('admin/css/custom.css',),
#     #     }
#     #     js = ('admin/js/custom.js',)

#     def save_model(self, request, obj, form, change):
#         if not obj.numero:
#             cliente = obj.proyecto.cliente
#             obj.numero = utils.get_correlative(
#                 constants.MODELO_PRESUPUESTO,
#                 cliente.iniciales,
#                 3)

#     #     instance.save()
#         super(BudgetAdmin, self).save_model(request, obj, form, change)


# @admin.register(models.TaskBudget)
# class TaskBudgetAdmin(admin.ModelAdmin):
#     models = models.TaskBudget
#     list_filter = ["budget__numero"]
#     ordering = ("position", )
#     list_display = ['wbs', 'nombre']
#     inlines = [
#         ManpowerTaskBudgetInline,
#         MaterialTaskBudgetInline,
#         EquipmentTaskBudgetInline
#     ]
