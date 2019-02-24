from django import forms

class ContactForm(forms.Form):
	full_name = forms.CharField(label='Your name', max_length=100,
		widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Full Name"}))
	email	  = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"E-mail"}))
	message	  = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"Content of message"}))


	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not "gmail.com" in email:
			raise forms.ValidationError("Email must be in domain gmail.com")
		return email