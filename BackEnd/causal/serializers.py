from rest_framework import serializers
from causal.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('uid',
                  'created_at',
                  'text',
                  'favorite_count',
                  'retweet_count',
                  'user_location',
                  'sentiment')
