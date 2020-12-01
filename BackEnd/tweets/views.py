from django.http.response import JsonResponse
from documents.forms import RequestForm
from rest_framework.decorators import api_view
from tweets.models import Tweet
from tweets.serializers import TweetSerializer


# Create your views here.
# Returns all tweets


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
