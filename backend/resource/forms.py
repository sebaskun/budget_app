# -*- coding: utf-8 -*-
from django import forms
from django_select2.forms import ModelSelect2Widget
import models
from ..budget import models

class ManpowerChoice(ModelSelect2Widget):
    model = models.Manpower
    search_fields = [
        'nombre__icontains',
    ]

class ManPowerBudgetModelForm(forms.ModelForm):

    class Meta:
        model = models.ManpowerBudget
        #fields = ('manoobra', 'precio', 'quantity', 'budget' )
        fields = '__all__'
        widgets = {
            'manoobra': ManpowerChoice(
                attrs={
                    'data-width': '30em'
                }
            ),
        }


# class ProjectChoices(ModelSelect2Widget):
#     model = models.Project
#     search_fields = [
#         'nombre__icontains',
#     ]
#
# class BudgetModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Budget
#         fields = '__all__'
#         widgets = {
#             'proyecto': ProjectChoices(
#                 attrs={
#                     'data-width': '50em'
#                     }
#             )
#         }
