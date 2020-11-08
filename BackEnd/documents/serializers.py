from rest_framework import serializers
from documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id',
                  'url',
                  'raw_HTML',
                  'title',
                  'text_body',
                  'cleaned_tokens',
                  'html_links')