from django import forms


class RequestForm(forms.Form):
    uid = forms.CharField(required=True, max_length=100)

