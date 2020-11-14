from django.shortcuts import render
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .serializers import FileSerializer
from .models import File
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser 
from rest_framework.response import Response
from rest_framework import status

# Source: https://medium.com/@emeruchecole9/uploading-images-to-rest-api-backend-in-react-js-b931376b5833
# Create your views here.

# views.py
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        print(files)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        files_serializer = FileSerializer(data=request.data)
        if files_serializer.is_valid():
            files_serializer.save()
            return Response(files_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', files_serializer.errors)
            return Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)