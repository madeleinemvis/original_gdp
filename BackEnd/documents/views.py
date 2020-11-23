from django.http.response import JsonResponse
from documents.models import Document
from documents.serializers import DocumentSerializer
from filehandler import FileHandler
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from functions.visualisation import DataVisualiser


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
        uid, claim, document_urls, document_pdfs, zip_file = file_handler.get_objects_from_request(request)
        # Fails if no UID or claim, or if no urls/pdfs/zip files in requests
        if not ((uid is None or claim is None) or
                (document_urls is None and document_pdfs is None and zip_file is None)):
            file_handler.save_claim(uid, claim)
            if document_urls:
                documents = file_handler.read_docs(document_urls)
                file_handler.save_documents(uid, 'web-page', documents)
            if document_pdfs:
                documents = file_handler.read_docs(document_pdfs)
                file_handler.save_documents(uid, 'pdf', documents)
            if zip_file:
                documents = file_handler.read_zip_file(uid, zip_file)
                # TODO: Is the content type remaining PDF?
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


def keywords_wordcloud(request):
    if request.method() == "GET":
        uid = request.data['uid']
        keywords = DataVisualiser.word_cloud(uid)
        return JsonResponse(data=keywords, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
