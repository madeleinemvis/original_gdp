from rest_framework import serializers 
from BackEnd.documents.models import Document
 
 
class DocumentSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Document
        fields = ('id',
                  'url',
                  'raw_HTML',
                  'meta_data',
                  'text_body',
                  'cleaned_tokens')