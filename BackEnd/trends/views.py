import json
from bson import json_util
from django.http.response import JsonResponse
from trends.forms import RequestForm
from functions.visualisation import DataVisualiser
from rest_framework import status
from rest_framework.decorators import api_view
from trends.models import Trend
from trends.serializers import TrendSerializer
from functions.viewshandler import ViewsHandler

