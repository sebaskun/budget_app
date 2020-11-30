# coding=utf-8
from __future__ import unicode_literals

# from dal import autocomplete

from django import forms

import models


# class UppercaseField(forms.CharField):
#     def to_python(self, value):
#         return value.upper()


class ClientForm(forms.ModelForm):

    class Meta:
        model = models.Client
        fields = "__all__"
