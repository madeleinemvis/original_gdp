import json
from bson import json_util
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from tweets.forms import RequestForm
from functions.visualisation import DataVisualiser
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from functions.viewshandler import ViewsHandler


@api_view(['POST'])
def tweets_list(request):
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            viewshandler = ViewsHandler()
            tweets = viewshandler.db_manager.get_all_tweets(uid)
            tweets = json.loads(json_util.dumps(tweets))
            return JsonResponse(data=tweets, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns tweets with Geo Locations
@api_view(['GET'])
def tweets_geo(request):
    tweets = Tweet.objects.exclude(user_location__exact='')
    twitter_serializer = TweetSerializer(tweets, many=True)
    return JsonResponse(twitter_serializer.data, safe=False)


@api_view(['POST'])
def tweet_frequency(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            frequency = datavisualiser.get_tweet_frequency(uid)
            return JsonResponse(data=frequency, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def tweet_summary(request):
    print("Tweet summary view call reached")
    if request.method == "POST":
        print("Request method == Post")
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            print("Request form is valid")
            datavisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            print("About to create summary")
            summary = datavisualiser.get_tweet_summary(uid)
            print("Tweet summary = ", summary)
            return JsonResponse(data=summary, status=status.HTTP_200_OK, safe=False)
    print("RETURNING HTTP 400 BAD REQUEST")
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def sentiment_scatter(request):
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            datavisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            tweets = datavisualiser.get_sentiment_scatter(uid)
            tweets = json.loads(json_util.dumps(tweets))
            return JsonResponse(data=tweets, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def sentiment_pie_chart(request):
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            dataVisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            sentiments = dataVisualiser.get_sentiment_pie_chart(uid)
            sentiments = json.loads(json_util.dumps(sentiments))
            return JsonResponse(data=sentiments, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def date_impact_bar(request):
    if request.method == "POST":
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            dataVisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            data = dataVisualiser.get_date_impact(uid)
            return JsonResponse(data=data, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
