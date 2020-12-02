from django import forms


class RequestForm(forms.Form):
    uid = forms.CharField(required=True, max_length=100)
    claim = forms.CharField(required=True, max_length=100)
    urls = forms.CharField(required=False)
    pdfs = forms.CharField(required=False)
    files = forms.FileField(required=False)


class SuggestionForm(forms.Form):
    want_suggestions = forms.BooleanField(required=True)
    urls = forms.CharField(required=False)
    pdfs = forms.CharField(required=False)
    files = forms.FileField(required=False)
