from rest_framework import serializers
from documents.models import Document
from documents.models import Tweet


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id',
                  'url',
                  'raw_HTML',
                  'text_body',
                  'cleaned_tokens')


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('created_at',
                  'text',
                  'favorite_count',
                  'user_location')
