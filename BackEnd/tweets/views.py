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


# Returns  JsonResponse wih all the Tweets under a specific UID as a dictionary
# The UID is passed into this function
@api_view(['POST'])
def tweets_list(request):
    if request.method == 'POST':
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            viewshandler = ViewsHandler()
            tweets = viewshandler.db_manager.get_all_tweets(uid)
            tweets = json.loads(json_util.dumps(tweets))
            return JsonResponse(data=tweets, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse with the query that was used to search the Tweets during the Crawling Process
# The UID is passed into this function
@api_view(['POST'])
def tweet_query(request):
    if request.method == 'POST':
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            viewshandler = ViewsHandler()
            query = viewshandler.db_manager.get_query(uid)
            return JsonResponse(data=query, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse of the number of Tweets collected under the UID
# The UID is passed into this function
@api_view(['POST'])
def tweet_frequency(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            frequency = datavisualiser.get_tweet_frequency(uid)
            return JsonResponse(data=frequency, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse with a summary of all Tweets under the UID: retweets, favourites and query used
# The UID is passed into this function
@api_view(['POST'])
def tweet_summary(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid = request_form.cleaned_data['uid']
            summary = datavisualiser.get_tweet_summary(uid)
            return JsonResponse(data=summary, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse with a dictionary of Tweets with: favourites, retweets and sentiments
# The UID is passed into this function
@api_view(['POST'])
def sentiment_scatter(request):
    if request.method == "POST":
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            datavisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            tweets = datavisualiser.get_sentiment_scatter(uid)
            print("tweets:", tweets)
            tweets = json.loads(json_util.dumps(tweets))
            return JsonResponse(data=tweets, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse with a dictionary of Tweets with sentiments
# The UID is passed into this function
@api_view(['POST'])
def sentiment_pie_chart(request):
    if request.method == "POST":
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            dataVisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            sentiments = dataVisualiser.get_sentiment_pie_chart(uid)
            sentiments = json.loads(json_util.dumps(sentiments))
            return JsonResponse(data=sentiments, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse with the combined retweets and favourites for the last 9 days
# The UID is passed into this function
@api_view(['POST'])
def date_impact_bar(request):
    if request.method == "POST":
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            dataVisualiser = DataVisualiser()
            uid = request_form.cleaned_data['uid']
            data = dataVisualiser.get_date_impact(uid)
            return JsonResponse(data=data, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
