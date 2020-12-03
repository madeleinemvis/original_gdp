from datetime import datetime

from django.http.response import JsonResponse
from documents.forms import RequestForm, SuggestionForm
from documents.models import Document
from documents.serializers import DocumentSerializer
from functions.filehandler import FileHandler
from functions.visualisation import DataVisualiser
from functions.overlordfunctions import Handler
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


@api_view(['POST'])
def upload_documents(request):
    # POSTING URLs and PDFs from request
    if request.method == 'POST':
        file_handler = FileHandler()
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            uid, claim, document_urls, document_pdfs, files = file_handler.get_objects_from_request(request, request_form)
            file_handler.set_claim(uid, claim)
            # FAILS if no documents attached
            if not (document_urls is None and document_pdfs is None and files is None):
                file_handler.save_claim(uid, claim)
                documents = None
                if document_urls:
                    documents = file_handler.read_docs(document_urls)
                    file_handler.save_documents(uid, 'web-page', documents)
                if document_pdfs:
                    documents = file_handler.read_docs(document_pdfs)
                    file_handler.save_documents(uid, 'pdf', documents)
                # if files:
                #    documents = file_handler.read_docs(files)
                #    file_handler.save_documents(uid, 'pdf', documents)
                return JsonResponse(data=uid, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(data=request.data,status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def suggest_urls(request):

    start_t = datetime.now()
    if request.method == 'POST':
        file_handler = FileHandler()
        suggestion_form = SuggestionForm(request.POST)
        if (suggestion_form.is_valid() and suggestion_form.cleaned_data['want_suggestions']):
            uid, claim, documents_urls, documents_pdfs, files = file_handler.get_objects_from_request(request, suggestion_form)
            # Convert data into Scraped Documents
            documents_urls = file_handler.read_docs(documents_urls)
            documents_pdfs = file_handler.read_docs(documents_pdfs)

            # TODO files
            # Merge document list
            documents = [*documents_urls, *documents_pdfs]
            handler = Handler()
            suggested_urls = handler.generate_suggested_urls(documents)
            print("Finished in: ", datetime.now()-start_t)
            return JsonResponse(data=suggested_urls, status=status.HTTP_201_CREATED, safe=False)
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
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        uid = request.data['uid']
        keywords = datavisualiser.word_cloud(uid)
        return JsonResponse(data=keywords, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
