from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
	full_name = forms.CharField()
	username = forms.CharField()
	email = forms.EmailField()
	password=forms.CharField(widget=forms.PasswordInput)
	repassword=forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data.get("username")
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username is taken")
		return username

	def clean_email(self):
		email = self.cleaned_data.get("email")
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("E-mail is taken")

		return email

	def clean(self):
		data = self.cleaned_data
		if data.get("password") != data.get("repassword"):
			raise forms.ValidationError("Passwords must match")
		return data


