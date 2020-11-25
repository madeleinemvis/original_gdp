from rest_framework import serializers
from documents.models import Document, Claim


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('uid',
                  'content_type',
                  'url',
                  'raw_html',
                  'title',
                  'text_body',
                  'cleaned_tokens',
                  'html_links')


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ('uid',
                  'claim')
