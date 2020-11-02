from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from documents.models import Document
from documents.serializers import DocumentSerializer
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def document_list(request):
    # GET list of documents, POST a new document, DELETE all documents
    if request.method == 'GET':
        documents = Document.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            documents = documents.filter(title__icontains=title)
        
        tutorials_serializer = DocumentSerializer(documents, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        document_data = JSONParser().parse(request)
        document_serializer = DocumentSerializer(data=document_data)
        if document_serializer.is_valid():
            document_serializer.save()
            return JsonResponse(document_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(document_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def document_detail(request, pk):
    # find document by pk (id)
    try: 
        document = Document.objects.get(pk=pk) 
    except Document.DoesNotExist: 
        return JsonResponse({'message': 'The document does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE document
    if request.method == 'GET': 
        document_serializer = DocumentSerializer(document) 
        return JsonResponse(document_serializer.data) 

    elif request.method == 'PUT': 
        document_data = JSONParser().parse(request) 
        document_serializer = DocumentSerializer(document, data=document_data) 
        if document_serializer.is_valid(): 
            document_serializer.save() 
            return JsonResponse(document_serializer.data) 
        return JsonResponse(document_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Document.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)