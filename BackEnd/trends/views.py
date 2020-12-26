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

@api_view(['POST'])
def econ_gauge(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            gauge = datavisualiser.get_causal_gauge(uid)
            return JsonResponse(data=gauge, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def health_gauge(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            gauge = datavisualiser.get_causal_gauge(uid)
            return JsonResponse(data=gauge, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def politics_gauge(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            gauge = datavisualiser.get_causal_gauge(uid)
            return JsonResponse(data=gauge, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def econ_bar(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            bar = datavisualiser.get_causal_bar(uid)
            return JsonResponse(data=bar, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def health_bar(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            bar = datavisualiser.get_causal_bar(uid)
            return JsonResponse(data=bar, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def politics_bar(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            bar = datavisualiser.get_causal_bar(uid)
            return JsonResponse(data=bar, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


