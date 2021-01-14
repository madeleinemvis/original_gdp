from django import forms


# Request Form for upload_documents and suggest_urls method in documents/views.py
# Validates the request's contents
class RequestForm(forms.Form):
    uid = forms.CharField(required=True, max_length=100)
    claim = forms.CharField(required=True, max_length=100)
    urls = forms.CharField(required=False)
    pdfs = forms.CharField(required=False)
    files = forms.FileField(required=False)

