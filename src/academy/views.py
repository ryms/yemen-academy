from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms.contact import ContactForm
from .forms.auth import LoginForm, RegisterForm



DEFAULT_TITLE = "Yemen academy"

User = get_user_model()

def home_page(request):
	context = {
	"title":DEFAULT_TITLE,
	"main_title":"Main page"
	}
	if request.user.is_authenticated:
		context["logged_in"] = "true"
		context["user"] = request.user
		print("logged in")
		print(request.user)
	return render(request, "home_page.html", context)

def about_page(request):
	context = {
	"title":DEFAULT_TITLE,
	"main_title":"About page"
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)

	context = {
	"title":DEFAULT_TITLE,
	"main_title":"Contact page",
	"form": contact_form
	}

	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	# if request.method == "POST":
	# 	#print(request.POST)
	# 	print(request.POST.get('full_name'))
	# 	print(request.POST.get('email'))
	# 	print(request.POST.get('message'))
	return render(request, "contact/view.html", context)

def login_page(request):
	form = LoginForm(request.POST or None)
	print("User logged in ")
	print(request.user.is_authenticated)
	
	if form.is_valid():
		username=form.cleaned_data.get("username")
		password=form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		print(request.user.is_authenticated)
		print(user)
		if user is not None:
			print(request.user.is_authenticated)
			login(request, user)
			#redirect to success page
			return redirect("/")
		else:
			#return an "invalid login" error message
			print("error")
	context = {
	"title":DEFAULT_TITLE,
	"main_title":"Login page",
	"form": form
	}
	return render(request, "auth/login.html", context)

def register_page(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)

	context = {
	"title":DEFAULT_TITLE,
	"main_title":"Register page",
	"form": form
	}

	if form.is_valid():
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")

		new_user = User.objects.create_user(username, email, password)
		login(request, new_user)
		#redirect to success page
		return redirect("/")

	return render(request, "auth/register.html", context)


def home_page_old(request):
	html = """
<h1>Hello World</h1>

	"""
	return HttpResponse(html)
