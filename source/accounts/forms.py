from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',  'email', 'first_name', 'last_name')

    def clean(self):
        super(UserRegisterForm, self).clean()
        if not self.cleaned_data.get("first_name") and not self.cleaned_data.get("last_name"):
            raise ValidationError('First name or Last name should be reqistered')
