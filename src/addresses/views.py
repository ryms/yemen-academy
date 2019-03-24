from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile

from .models import Address

from .forms import AddressForm

def checkout_address_create_view(request):
	form  = AddressForm(request.POST or None)
	context={
		"form":form
	}

	next_url_get = request.GET.get('next_url')
	next_url_post = request.POST.get('next_url')

	redirect_path = next_url_get or next_url_post or None
	if form.is_valid():
		print(request.POST)
		instance=form.save(commit=False)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if billing_profile is not None:
			instance.billing_profile = billing_profile
			address_type = request.POST.get('address_type', 'shipping')
			instance.address_type = address_type
			instance.save()

			request.session[address_type + "_address_id"]=instance.id

		else:
			print("Error when save data")
			return redirect("cart:checkout")

		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)

	return redirect("cart:checkout")


def checkout_address_reuse_view(request):
	if request.user.is_authenticated:
		context = {}
	next_url_get = request.GET.get('next_url')
	next_url_post = request.POST.get('next_url')
	redirect_path = next_url_get or next_url_post or None

	if request.method=="POST":
		address_id=request.POST.get("address_id", None)
		address_type=request.POST.get("address_type", "shipping")
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if address_id is not None:
			qs=Address.objects.filter(billing_profile=billing_profile, id=address_id)
			if qs.exists():
				request.session[address_type + "_address_id"]=address_id
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)

	return redirect("cart:checkout")









