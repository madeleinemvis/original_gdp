from django import forms


# Request Form for all functions in tweets/views.py
# Validates the request's contents
class RequestForm(forms.Form):
    uid = forms.CharField(required=True, max_length=100)

