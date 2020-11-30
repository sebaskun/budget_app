# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

# # from datetime import date
# # from copy import deepcopy

from django.contrib import admin
from django.utils.html import format_html

from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
# import nested_admin

from . import models


# class MeansContactInline(nested_admin.NestedTabularInline):
#     model = models.MeansContact
#     sortable_field_name = "position"
#     extra = 0


# class ContactInline(nested_admin.NestedTabularInline):
#     model = models.Contact
#     sortable_field_name = "position"
#     fields = ("nombre", "cargo", "observacion", "position")
#     extra = 0
#     inlines = [MeansContactInline]


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    """
    """
    list_display = [
        'name',
        'view_logo',
    ]
    # inlines = [ContactInline]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'short_name',),
                ('initials', 'ruc',), 'address', 'logo'),
         }),
    )

    def view_logo(self, obj):
        if obj.logo:
            try:
                thumb_url = get_thumbnailer(obj.logo)['avatar'].url
                return format_html(
                        """
                            <img src='{}'>
                        """, thumb_url)
            except InvalidImageFormatError:
                return "Sin imagen"
        else:
            return "Sin imagen"
    view_logo.short_description = "Logo"
