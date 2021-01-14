from django.http.response import JsonResponse
from functions.visualisation import DataVisualiser
from rest_framework import status
from rest_framework.decorators import api_view
from trends.forms import RequestForm


@api_view(['POST'])
def econ_gauge(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            g = datavisualiser.get_causal_gauge(uid)
            gauge = dict({'value': g['econ']})
            return JsonResponse(data=gauge, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def health_gauge(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            g = datavisualiser.get_causal_gauge(uid)
            gauge = dict({'value': g['health']})
            return JsonResponse(data=gauge, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def politics_gauge(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            g = datavisualiser.get_causal_gauge(uid)
            gauge = dict({'value': g['politics']})
            return JsonResponse(data=gauge, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def econ_bar(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            b = datavisualiser.get_causal_bar(uid)
            bar = dict({'estimate': b['econ_estimate'], 'random': b['econ_random'],
                       'unobserved': b['econ_unobserved'], 'placebo': b['econ_placebo'], 'subset': b['econ_subset']})
            return JsonResponse(data=bar, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def health_bar(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            b = datavisualiser.get_causal_bar(uid)
            bar = dict({'estimate': b['health_estimate'], 'random': b['health_random'],
                        'unobserved': b['health_unobserved'], 'placebo': b['health_placebo'], 'subset': b['health_subset']})
            return JsonResponse(data=bar, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def politics_bar(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            b = datavisualiser.get_causal_bar(uid)
            bar = dict({'estimate': b['politics_estimate'], 'random': b['politics_random'],
                        'unobserved': b['politics_unobserved'], 'placebo': b['politics_placebo'],
                        'subset': b['politics_subset']})
            return JsonResponse(data=bar, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['POST'])
def trend_map(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            m = datavisualiser.get_trend_map(uid)
            tmap = dict({'countries': m['countries'], 'trends': m['trends']})
            return JsonResponse(data=tmap, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)

