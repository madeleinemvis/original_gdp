from datetime import datetime

from django.http.response import JsonResponse
from documents.forms import RequestForm
from documents.models import Document
from documents.serializers import DocumentSerializer
from filehandler import FileHandler
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from functions.visualisation import DataVisualiser


@api_view(['POST'])
def document_list(request):
    # POSTING URLs and PDFs from request
    if request.method == 'POST':
        file_handler = FileHandler()
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            uid, claim, document_urls, document_pdfs, zip_file = file_handler.get_objects_from_request(request, request_form)
            # FAILS if no documents attached
            if not(document_urls is None and document_pdfs is None and zip_file is None):
                file_handler.save_claim(uid, claim)
                if document_urls:
                    documents = file_handler.read_docs(document_urls)
                    file_handler.save_documents(uid, 'web-page', documents)
                if document_pdfs:
                    documents = file_handler.read_docs(document_pdfs)
                    file_handler.save_documents(uid, 'pdf', documents)
                if zip_file:
                    documents = file_handler.read_zip_file(uid, zip_file)
                    file_handler.save_documents(uid, 'pdf', documents)
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

@api_view(['POST'])
def keywords_wordcloud(request):
    start_t = datetime.now()
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        uid = request.data['uid']
        data = datavisualiser.word_cloud(uid)
        response = JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        print("Time taken to complete request: ", datetime.now()-start_t)
        return response
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)