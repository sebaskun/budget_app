# coding=utf-8
from __future__ import unicode_literals

from dal import autocomplete
import xml.etree.ElementTree as ET

# import untangle

from django import forms
from django.core.validators import FileExtensionValidator

from . import models
# from django_select2.forms import ModelSelect2Widget
from datetime import datetime

from ..project.models import Project
from ..core.models import Correlative, constants
from ..core.utils import get_correlative


class TaskInlineForm(forms.ModelForm):
    wbs = forms.CharField(widget=forms.TextInput(attrs={'class': 'col-wbs'}))
    rendimiento = forms.CharField(widget=forms.TextInput(attrs={'class': 'col-rendimiento'}))
    unidad = forms.CharField(widget=forms.TextInput(attrs={'class': 'col-unidad'}), required=False)
    cantidad = forms.CharField(widget=forms.TextInput(attrs={'class': 'col-cantidad'}))
    fecha_inicio_proyectada = forms.DateField(widget=forms.DateInput(attrs={'class': 'vDateField hasDatepicker col-fecha'}))
    fecha_termino_proyectada = forms.DateField(widget=forms.DateInput(attrs={'class': 'vDateField hasDatepicker col-fecha'}))

    class Meta:
        model = models.TaskBudget
        fields = "__all__"

    class Media:
        css = {
            'all': ('budget/css/task.css',)
        }

    def __init__(self, *args, **kwargs):
        super(TaskInlineForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget = forms.HiddenInput()


class UppercaseField(forms.CharField):
    def to_python(self, value):
        return value.upper()


class BudgetForm(forms.ModelForm):
    numero = UppercaseField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'})
        )

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        # qs = qs.filter(fecha_presentacion_propuesta__year__gte=current_year)
        self.fields['proyecto'].queryset = Project.objects.filter(fecha_presentacion_propuesta__year__gte=current_year)
        self.fields['position'].widget = forms.HiddenInput()
        self.fields['numero'].widget = forms.HiddenInput()
        self.fields['estado'].widget = forms.HiddenInput()

    class Meta:
        model = models.Budget
        fields = "__all__"


class ImportXMLForm(forms.Form):

    CHOICES = [
        ('1', 'Crear como nuevas tareas'),
        ('2', 'Combinar tareas importadas con las actuales')]

    file = forms.FileField(
        label="Archivo",
        validators=[FileExtensionValidator(allowed_extensions=['xml'])])
    accion = forms.ChoiceField(
        label="Acción",
        choices=CHOICES,
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super(ImportXMLForm, self).__init__(*args, **kwargs)
        self.initial['accion'] = '1'

    def form_action(self, budget, user):
        raise NotImplementedError()

    def save(self, budget, user):

        tree = ET.parse(self.cleaned_data["file"])
        action = self.cleaned_data["accion"]
        root = tree.getroot()
        ns = {'ns': 'http://schemas.microsoft.com/project'}
        # fields = [
        #     "WBS",
        #     "Name",
        #     # "UID",
        #     # "ID",
        #     # "Active",
        #     # "Manual"
        #     # "OutlineLevel",
        #     "Start",
        #     "Finish",
        #     # "RemainingDuration",
        #     # ("PredecessorLink", "PredecessorUID")
        # ]

        # La opción 1 indica que se borrará todas las tareas antes de actualizarla.
        if action == "1":
            models.TaskBudget.objects.filter(budget_id=budget.pk).delete()
        xml_tasks = root.find('ns:Tasks', ns)
        if xml_tasks is not None:
            for item in xml_tasks:
                wbs = item.find('ns:WBS', ns).text if item.find('ns:WBS', ns) is not None else None
                if wbs:
                    nombre = item.find('ns:Name', ns).text if item.find('ns:Name', ns) is not None else "-"
                    nombre = nombre.encode("utf-8")
                    fecha_inicio = item.find('ns:Start', ns).text if item.find('ns:Start', ns) is not None else None
                    fecha_fin = item.find('ns:Finish', ns).text if item.find('ns:Finish', ns) is not None else None
                    # print "wbs: ", wbs, "nombre: ", nombre, "inicio: ", fecha_inicio, "fin: ", fecha_fin

                    task, is_new = models.TaskBudget.objects.get_or_create(budget_id=budget.pk, wbs=wbs)
                    task.nombre = nombre
                    if fecha_inicio:
                        task.fecha_inicio_proyectada = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
                    if fecha_fin:
                        task.fecha_termino_proyectada = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
                    task.save()


class ManpowerBudgetModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ManpowerBudgetModelForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget = forms.HiddenInput()

    class Meta:
        model = models.ManpowerBudget
        fields = "__all__"
