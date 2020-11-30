# coding=utf-8
from __future__ import unicode_literals

from django.utils.http import is_safe_url

from datetime import datetime

from django.db import models

# from pathlib import Path

# import csv

# from apps.resource.models import Manpower


def get_correlative(type_doc, prefix, length=3):
    from .models import Correlative
    obj, created = Correlative.objects.get_or_create(
        model=type_doc,
        prefix=prefix
    )
    new_number = obj.current_number + 1
    obj.current_number = new_number
    obj.save()
    return '{prefijo}-{num:0{len}d}'.format(num=new_number, prefijo=prefix, len=length)


def get_date_format(date=None):
    date_now = date or datetime.today()
    format_year = ""
    format_month = "%m"
    format_day = "%d"
    year_now = datetime.today().year
    # month_now = datetime.today().month
    if date_now.year != year_now:
        format_year = "%Y"
    # if date_now.month != month_now:
    #     format_month = "%b"

    if format_year:
        return "{0}/{1}/{2}".format(format_day, format_month, format_year)

    return "{0} {1}.".format(format_day, format_month)


def is_number(s):
    if s:
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

    return False


def next_url(request):
    """
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next = request.GET.get("next", request.POST.get("next", ""))
    host = request.get_host()
    return next if next and is_safe_url(next, host=host) else None


class CharNullField(models.CharField):
    description = "CharField that stores NULL"

    def get_db_prep_value(self, value, connection=None, prepared=False):
        value = super(CharNullField, self).get_db_prep_value(value, connection, prepared)
        if value == "":
            return None
        else:
            return value



# def import_manpower_csv(file=None):
#     my_file = Path(file)
#     if not my_file.is_file():
#         return

#     with open(my_file) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['code'] is not "":
#                 manpower, created = Manpower.objects.get_or_create(
#                     code=row['code'],
#                     defaults={'currency': 'D',
#                         'name': '--'}
#                 )
#                 if row['name'] is not "":
#                     manpower.name = row['name'].upper()
#                 if row['cost'] is not "":
#                     manpower.name = Decimal(row['cost'])


