from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from rest_framework.decorators import api_view


# Create your views here.
# Returns all tweets
@api_view(['GET'])
def tweets_list(request):
    tweets = Tweet.objects.all()
    twitter_serializer = TweetSerializer(tweets, many=True)
    return JsonResponse(twitter_serializer.data, safe=False)


# Returns tweets with Geo Locations
@api_view(['GET'])
def tweets_geo(request):
    tweets = Tweet.objects.exclude(user_location__exact='')
    twitter_serializer = TweetSerializer(tweets, many=True)
    return JsonResponse(twitter_serializer.data, safe=False)
