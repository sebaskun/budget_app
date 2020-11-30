# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404

import xml.etree.ElementTree as ET
from xml.dom import minidom
from constance import config
from .models import Budget


import datetime

xmlns = {"xmlns": "http://schemas.microsoft.com/project"}

root_head = {
    "SaveVersion": "14",
    "Name": "ejemplo.xml",
    "CurrencyDigits": "2",
    "CurrencySymbol": "S/",
    "CurrencyCode": "PEN",
    "CalendarUID": "1",
    "DefaultStartTime": "09:00:00",
    "DefaultFinishTime": "19:00:00",
    "MinutesPerDay": "480",
    "MinutesPerWeek": "2400",
    "DaysPerMonth": "20",
    "StartDate": "2018-01-13T09:00:00",
    "FinishDate": "2018-02-01T19:00:00"
}

calendar_dict = {
    "UID": "1",
    "Name": "Estándar",
}


task_dict = {
    "UID": None,
    "ID": None,
    "Name": None,
    "Active": "1",
    "Manual": "1",
    "WBS": None,
    "OutlineLevel": None,
    "Priority": "500",
    "Start": None,
    "Finish": None,
    "RemainingDuration": "PT16H0M0S",  # Hacer el calculo
}

resource_dict = {
    "UID": None,
    "ID": None,
    "Name": None,
    "Type": None,  # 0 Mano de obra, 1 Material, 2 Servicio
    "StandardRate": None,  # Costo
    "StandardRateFormat": "2"
}

assignment_dict = {
    "UID": None,
    "TaskUID": None,
    "ResourceUID": None,
    "Units": None,
    "Work": None
}

offset_manpower = 0
offset_material = 10000
offset_equipment = 20000


def build_budget_xml(budget_id):
    """
    Construye una estructura XML para la descarga
    """
    budget = get_object_or_404(Budget, pk=budget_id)
    if budget:

        date_max = budget.get_date_max['projected_finish_date__max'].strftime(
            "%Y-%m-%d") + "T" + config.DEFAULT_FINISH_TIME.strftime("%H:%M:%S")
        date_min = budget.get_date_min['projected_start_date__min'].strftime(
            "%Y-%m-%d") + "T" + config.DEFAULT_START_TIME.strftime("%H:%M:%S")

        # Crear cabecera
        root = ET.Element('Project', attrib=xmlns)
        children = []
        for (key, value) in root_head.items():
            item = ET.Element(key)
            if key == "DefaultStartTime":
                item.text = config.DEFAULT_START_TIME.strftime("%H:%M:%S")
            elif key == "DefaultFinishTime":
                item.text = config.DEFAULT_FINISH_TIME.strftime("%H:%M:%S")
            elif key == "StartDate":
                item.text = date_min
            elif key == "FinishDate":
                item.text = date_max
            else:
                item.text = value
            children.append(item)
        root.extend(children)
        # Crear calendarios
        calendars = ET.SubElement(root, "Calendars")
        calendar = ET.SubElement(calendars, "Calendar")
        for (key, value) in calendar_dict.items():
            item = ET.Element(key)
            item.text = value
            calendar.append(item)
        # Crear tareas
        tasks_model = budget.tasks_budget.all().order_by('position')
        tasks = ET.SubElement(root, "Tasks")
        index = 0
        for task_model in tasks_model:
            index += 1
            # add_key = True
            task = ET.SubElement(tasks, "Task")
            for (key, value) in task_dict.items():
                item = ET.Element(key)
                if key == "UID":
                    item.text = str(task_model.id)
                elif key == "ID":
                    item.text = str(index)
                elif key == "WBS":
                    item.text = task_model.wbs
                elif key == "Name":
                    item.text = task_model.name
                elif key == "Type":
                    item.text = "1"
                elif key == "OutlineLevel":
                    item.text = str(task_model.get_outline_level)
                elif key == "Start":
                    item.text = task_model.projected_start_date.strftime(
                        "%Y-%m-%dT") + config.DEFAULT_FINISH_TIME.strftime("%H:%M:%S")
                elif key == "Finish":
                    item.text = task_model.projected_finish_date.strftime(
                        "%Y-%m-%dT") + config.DEFAULT_START_TIME.strftime("%H:%M:%S")
                elif key == "RemainingDuration":
                    item.text = task_model.get_diff_dates_formatted
                # elif key == "Manual":
                #     if task_model.has_children:
                #         item = None
                else:
                    item.text = value

                if item is not None:
                    task.append(item)
        # Crear recursos
        resources = ET.SubElement(root, "Resources")
        # Mano de obra
        resources_model = budget.manpowers_budget.all()
        index = 0
        for resource_model in resources_model:
            index += 1
            resource = ET.SubElement(resources, "Resource")
            for (key, value) in resource_dict.items():
                item = ET.Element(key)
                if key == "UID":
                    item.text = str(resource_model.manpower.id + offset_manpower)
                elif key == "ID":
                    item.text = str(index)
                elif key == "Name":
                    item.text = resource_model.manpower.name
                elif key == "Type":
                    item.text = "1"  # Mano de obra
                elif key == "StandardRate":
                    item.text = str(resource_model.precio)
                elif key == "StandardRateFormat":
                    item.text = "2"
                else:
                    item.text = value

                if item is not None:
                    resource.append(item)

        # Material
        resources_model = budget.materials_budget.all()
        # index = 0
        for resource_model in resources_model:
            index += 1
            resource = ET.SubElement(resources, "Resource")
            for (key, value) in resource_dict.items():
                item = ET.Element(key)
                if key == "UID":
                    item.text = str(resource_model.material.id + offset_material)
                elif key == "ID":
                    item.text = str(index)
                elif key == "Name":
                    item.text = resource_model.material.name
                elif key == "Type":
                    item.text = "0"  # Material
                elif key == "StandardRate":
                    item.text = str(resource_model.precio)
                elif key == "StandardRateFormat":
                    item.text = "2"
                else:
                    item.text = value

                if item is not None:
                    resource.append(item)

        # Equipos
        resources_model = budget.equipments_budget.all()
        # index = 0
        for resource_model in resources_model:
            index += 1
            resource = ET.SubElement(resources, "Resource")
            for (key, value) in resource_dict.items():
                item = ET.Element(key)
                if key == "UID":
                    item.text = str(resource_model.equipo.id + offset_equipment)
                elif key == "ID":
                    item.text = str(index)
                elif key == "Name":
                    item.text = resource_model.equipo.name
                elif key == "Type":
                    item.text = "1"  # Costo por hora
                elif key == "StandardRate":
                    item.text = str(resource_model.precio)
                elif key == "StandardRateFormat":
                    item.text = "2"
                else:
                    item.text = value

                if item is not None:
                    resource.append(item)

        # Crear asignaciones
        assignments = ET.SubElement(root, "Assignments")
        # Mano de obra
        tasks_model = budget.tasks_budget.all()
        for task in tasks_model:
            assignments_model = task.manpowers_task_budget.all()
            for assignment_model in assignments_model:
                assignment = ET.SubElement(assignments, "Assignment")
                for (key, value) in assignment_dict.items():
                    item = ET.Element(key)
                    if key == "UID":
                        item.text = str(assignment_model.id)
                    elif key == "TaskUID":
                        item.text = str(assignment_model.tarea.id)
                    elif key == "ResourceUID":
                        item.text = str(assignment_model.manpower.id + offset_manpower)
                    elif key == "Units":
                        item.text = str(assignment_model.get_factor)
                    elif key == "StandardRateFormat":
                        item.text = "2"
                    else:
                        item.text = value

                    if item is not None:
                        assignment.append(item)

    root_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(root_string)

    return reparsed.toprettyxml(indent="    ")
