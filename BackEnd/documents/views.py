from datetime import datetime

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .forms import RequestForm
from .models import Document
from .serializers import DocumentSerializer
from functions.programhandler import Handler
from functions.viewshandler import ViewsHandler
from functions.visualisation import DataVisualiser


# This function is the main function used when the web-app sends a upload request to the web-server
# This function validates the files, and scrapes the files' contents and html-links
# This function then calls run_program from the Handler object, to begin the crawling/scraping/analysis
@api_view(['POST'])
def upload_documents(request):
    # Checks request method
    if request.method == 'POST':
        views_handler = ViewsHandler()
        # validates all attachments match form
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            # extracts data from request
            uid, claim, documents_urls, documents_pdfs, files = views_handler.get_objects_from_request(request,
                                                                                                       request_form)
            # FAILS if no documents attached
            if not (documents_urls is None and documents_pdfs is None and files is None):
                # Convert each file into Document model object with views.handler.read_docs()
                if documents_urls:
                    documents_urls = views_handler.read_docs(documents_urls)  # List of inputted URLs
                if documents_pdfs:
                    documents_pdfs = views_handler.read_docs(documents_pdfs)  # List of inputted PDF URLs
                if files:
                    files = views_handler.read_docs(files)  # List of inputted Django.TemporaryUploadedFile objects

                documents = [*documents_urls, *documents_pdfs, *files]
                handler = Handler()
                start_t = datetime.now()
                try:
                    # Runs scraper/crawler/analysis
                    handler.run_program(views_handler, uid, claim, documents)
                except Exception as e:
                    print("views.py e:", e)
                    return JsonResponse(data=request.data, status=status.HTTP_400_BAD_REQUEST, safe=False)
                print("TOTAL TIME TAKEN:", datetime.now() - start_t)
                return JsonResponse(data=uid, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(data=request.data, status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse of a list of URLs
@api_view(['POST'])
def suggest_urls(request):
    # Checks request method
    if request.method == 'POST':
        views_handler = ViewsHandler()
        # validates all attachments match form
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            # extracts data from request
            uid, claim, documents_urls, documents_pdfs, files = views_handler.get_objects_from_request(request,
                                                                                                       request_form)
            # Convert each file into Document model object with views.handler.read_docs()
            if documents_urls:
                documents_urls = views_handler.read_docs(documents_urls)
            if documents_pdfs:
                documents_pdfs = views_handler.read_docs(documents_pdfs)
            if files:
                files = views_handler.read_docs(files)

            documents = [*documents_urls, *documents_pdfs, *files]
            handler = Handler()
            # Generates list of suggested URLs to be POSTed
            suggested_urls = handler.generate_suggested_urls(documents)
            return JsonResponse(data=suggested_urls, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(data=request.data, status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse of a dictionary representing a list of documents
# The UID is passed into this function
@api_view(['POST'])
def document_list(request):
    if request.method == "POST":
        datavisualiser = DataVisualiser()
        uid = request.data["uid"]
        documents = datavisualiser.get_all_documents(uid)
        return JsonResponse(data=documents, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse of a list of keywords
# The UID is passed into this function
@api_view(['POST'])
def keywords_wordcloud(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        uid = request.data['uid']
        keywords = datavisualiser.word_cloud(uid)
        return JsonResponse(data=keywords, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)


# Returns a JsonResponse with the number of documents stored in the DB under the UID given
# The UID is passed into this function
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


@api_view(['POST'])
def website_graph(request):
    datavisualiser = DataVisualiser()
    if request.method == "POST":
        uid = request.data['uid']
        graph = datavisualiser.get_website_graph(uid)
        graph = graph.replace('\'', '"').lower()
        return JsonResponse(data=graph, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, safe=False)
