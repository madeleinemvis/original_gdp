from django.http.response import JsonResponse
from documents.forms import RequestForm
from functions.visualisation import DataVisualiser
from rest_framework import status
from rest_framework.decorators import api_view
from tweets.models import Tweet
from tweets.serializers import TweetSerializer


@api_view(['POST'])
def tweets_list(request):
    request_form = RequestForm(request.POST, request.FILES)
    tweets = Tweet.objects.all()
    twitter_serializer = TweetSerializer(tweets, many=True)
    return JsonResponse(twitter_serializer.data, safe=False)


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
        uid = request.data['uid']
        frequency = datavisualiser.get_tweet_frequency(uid)
        return JsonResponse(data=frequency, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
