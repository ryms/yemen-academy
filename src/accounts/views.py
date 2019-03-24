from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from django.conf import settings

def guest_register_view(request):
	form = GuestForm(request.POST or None)
	context= {"form":form}
	url_next_get = request.GET.get('next')
	url_next_post = request.POST.get('next')
	redirect_path = url_next_get or url_next_post or None
	if form.is_valid():
		email=form.cleaned_data.get("email")
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = new_guest_email.id
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			#redirect to register page
			return redirect("/register/")
	else:
		return redirect("/register/")


def login_page(request):
	form = LoginForm(request.POST or None)
	print("User logged in ")
	print(request.user.is_authenticated)

	url_next_get = request.GET.get('next')
	url_next_post = request.POST.get('next')
	redirect_path = url_next_get or url_next_post or None
	
	if form.is_valid():
		username=form.cleaned_data.get("username")
		password=form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				#redirect to success page
				return redirect("/")
		else:
			#return an "invalid login" error message
			print("error")
	context = {
	"title":settings.DEFAULT_TITLE,
	"main_title":"Login page",
	"form": form
	}
	return render(request, "accounts/login.html", context)

def register_page(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)

	context = {
	"title":settings.DEFAULT_TITLE,
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

	return render(request, "accounts/register.html", context)