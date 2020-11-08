from rest_framework import serializers
from tweets.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('created_at',
                  'text',
                  'favorite_count',
                  'retweet_count',
                  'user_location',
                  'sentiment')
