from django import forms
from django.forms import widgets
from webapp.models import Status, Type, List


class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['summary', 'description', 'status', 'tip']

