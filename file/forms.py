from platform import node

from django import forms
from django.contrib.auth.forms import UserCreationForm

from file.models import Account, FileSystem


class AddFileForm(forms.Form):
	name = forms.CharField(max_length=50, help_text='*Required')
	parent = forms.ModelChoiceField(queryset=FileSystem.objects.all())


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text="Required. Add a valid email")

	class Meta:
		model = Account
		fields = ("email", "username", "password", "display_name")


class LoginForm(forms.Form):
	username = forms.CharField(max_length=25)
	password = forms.CharField(widget=forms.PasswordInput)
