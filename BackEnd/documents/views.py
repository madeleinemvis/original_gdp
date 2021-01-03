from datetime import datetime
from django.http.response import JsonResponse
from documents.forms import RequestForm
from documents.models import Document
from documents.serializers import DocumentSerializer
from functions.visualisation import DataVisualiser
from functions.programhandler import Handler
from functions.viewshandler import ViewsHandler
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


@api_view(['POST'])
def upload_documents(request):
    # POSTING URLs and PDFs from request
    if request.method == 'POST':
        views_handler = ViewsHandler()
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            uid, claim, documents_urls, documents_pdfs, files = views_handler.get_objects_from_request(request,
                                                                                                       request_form)
            views_handler.set_claim(uid, claim)
            # FAILS if no documents attached
            if not (documents_urls is None and documents_pdfs is None and files is None):
                views_handler.save_claim(uid, claim)
                if documents_urls:
                    documents_urls = views_handler.read_docs(documents_urls)
                if documents_pdfs:
                    documents_pdfs = views_handler.read_docs(documents_pdfs)
                if files:
                    files = views_handler.read_docs(files)

                documents = [*documents_urls, *documents_pdfs, *files]
                handler = Handler()
                start_t = datetime.now()
                print("Starting program")
                try:
                    handler.run_program(views_handler, uid, documents)
                except Exception as e:
                    print("e:", e)
                print("TOTAL TIME TAKEN:", datetime.now() - start_t)
                return JsonResponse(data=uid, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(data=request.data, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def suggest_urls(request):
    if request.method == 'POST':
        views_handler = ViewsHandler()
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            uid, claim, documents_urls, documents_pdfs, files = views_handler.get_objects_from_request(request,
                                                                                                       request_form)
            # Convert data into Scraped Documents
            if documents_urls:
                documents_urls = views_handler.read_docs(documents_urls)
            if documents_pdfs:
                documents_pdfs = views_handler.read_docs(documents_pdfs)
            if files:
                files = views_handler.read_docs(files)
            # Merge document list
            documents = [*documents_urls, *documents_pdfs, *files]
            handler = Handler()
            suggested_urls = handler.generate_suggested_urls(documents)
            return JsonResponse(data=suggested_urls, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(data=request.data, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def document_list(request):
    if request.method == "POST":
        datavisualiser = DataVisualiser()
        uid = request.data["uid"]
        documents = datavisualiser.get_all_documents(uid)
        return JsonResponse(data=documents, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def keywords_wordcloud(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        uid = request.data['uid']
        keywords = datavisualiser.word_cloud(uid)
        print(keywords)
        return JsonResponse(data=keywords, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def document_frequency(request):
    if request.method == "POST":
        datavisualiser = DataVisualiser()
        uid = request.data['uid']
        frequency = datavisualiser.get_document_frequency(uid)
        return JsonResponse(data=frequency, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def document_frequency(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        uid = request.data['uid']
        frequency = datavisualiser.get_document_frequency(uid)
        return JsonResponse(data=frequency, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
