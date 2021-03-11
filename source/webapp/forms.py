from django import forms
from django.forms import widgets
from webapp.models import Status, Type


class ListForm(forms.Form):
    summary = forms.CharField(max_length=100, label='Заголовок')
    description = forms.CharField(max_length=3000, widget=widgets.Textarea(), required=False, label='Описание')
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    tip = forms.ModelChoiceField(queryset=Type.objects.all())