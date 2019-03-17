from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
	username=forms.CharField(label='User name', max_length=100,
		widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"username"}))

	password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class RegisterForm(forms.Form):
	full_name = forms.CharField(label='Full name', max_length=100,
		widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Full name"}))
	
	username = forms.CharField(label='User name', max_length=100,
		widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"username"}))
	
	email = forms.EmailField(label='E-mail', max_length=100,
		widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"E-mail"}))

	password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
	repassword=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

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
