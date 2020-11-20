import json

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from documents.models import Document
from documents.serializers import DocumentSerializer
from rest_framework.decorators import api_view
from filehandler import FileHandler


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
    # Retrieving URLs and PDFs from request
    elif request.method == 'POST':
        file_handler = FileHandler()

        uid = request.data['uid']
        document_urls = request.data['urls']
        document_pdfs = request.data['pdfs']
        zip_file = request.FILES['files']
        # If there are URLs
        if document_urls:
            print("urls")
            # Scrapes all URLs, UID for manifesto and list of Documents (namedtuple)
            documents = file_handler.read_docs(document_urls)
            # Store scraped Documents
            d_save = file_handler.set_documents(uid, documents)
            Document.objects.bulk_create(d_save)

        if document_pdfs:
            print("pdfs")
            # Scrapes all PDFs
            documents = file_handler.read_docs(document_pdfs)
            # Store scraped documents
            d_save = file_handler.set_documents(uid, documents)
            Document.objects.bulk_create(d_save)

        if zip_file:
            print("zip files")
            # Extract, read and process all documents
            documents = file_handler.read_zip_file(uid, zip_file)
            d_save = file_handler.set_documents(uid, documents)
            Document.objects.bulk_create(d_save)

        return JsonResponse(data=request.data, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


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
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)
