from django import forms
from django.forms import widgets
from webapp.models import Projects, List


class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['summary', 'description', 'status', 'tip']


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['name', 'description', 'created_date', 'update_date']


class ProjectsUpdateForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['name', 'description', 'created_date', 'update_date']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['user']