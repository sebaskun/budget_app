# -*- coding: utf-8 -*-
# from decimal import Decimal
# import shelve
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import JsonResponse
# from django.forms.models import model_to_dict


from rest_framework import (
    pagination
)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
