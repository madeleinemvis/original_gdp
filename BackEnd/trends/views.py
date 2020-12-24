import json
from bson import json_util
from django.http.response import JsonResponse
from trends.forms import RequestForm
from functions.visualisation import DataVisualiser
from rest_framework import status
from rest_framework.decorators import api_view
from trends.models import Tweet
from trends.serializers import TweetSerializer
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
