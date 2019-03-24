from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart,ProductInCart
from billing.models import BillingProfile
from addresses.models import Address

from accounts.views import LoginForm, GuestForm
from addresses.forms import AddressForm

from orders.models import Order
from accounts.models import GuestEmail

def cart_create(user=None):
	cart_id = request.session.get("cart_id", None)
	if cart_id is not None and isinstance(cart_id, int):
		cart_obj = Cart.objects.get(id = cart_id)
	else:
		cart_obj = Cart.objects.create(user=user)
		request.session['cart_id'] = cart_obj.id
		print("New cart created")

	return cart_obj

def cart_home(request):
	cart_obj,new_obj = Cart.objects.new_or_get(request)
	productsInCart = cart_obj.cart_items.all()
	count = 0
	for prodInCart in productsInCart:
		count +=prodInCart.count_item
	
	request.session['cart_items'] = count
	context={"cart":cart_obj}
	return render(request, "carts/home.html", context)


def cart_update(request):
	product_id = request.POST.get('product')
	try:
		product_obj = Product.objects.get(id = product_id)
	except Product.DoesNotExist:
		print("Product with id {} not found".format(product_id))
		return redirect("cart:home")
		
	action = None

	if 'delete' in request.POST:
		action = "delete"
	elif 'add' in request.POST:
		action = "add"
	elif 'update' in request.POST:
		action = "update"

	count = int(request.POST.get('count', 0))

	Cart.objects.update(request, product_obj, count, action)

	
	return redirect("cart:home")


def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	print("count items : {count}".format(count = cart_obj.cart_items.count()))
	if cart_created or cart_obj.cart_items.count() == 0:
		return redirect("cart:home")

	user = request.user
	login_form = LoginForm()
	guest_form = GuestForm()
	address_form = AddressForm()

	billing_address_id = request.session.get("billing_address_id", None)
	shipping_address_id = request.session.get("shipping_address_id", None)

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	address_qs = None

	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile = billing_profile)

		order_obj,order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if order_obj_created:
			del request.session["order_number"]
			del request.session["order_email"]

		if shipping_address_id is not None:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]

		if billing_address_id is not None:
			order_obj.billing_address = Address.objects.get(id = billing_address_id)
			del request.session["billing_address_id"]

		if billing_address_id or shipping_address_id:
			order_obj.save()

	if request.method=="POST":
		is_done = order_obj.check_done()
		if is_done:
			order_obj.mark_paid()
			del request.session["cart_id"]
			request.session["cart_items"] = 0
			request.session["order_number"] = order_obj.order_id
			request.session["order_email"] = billing_profile.email
			# generate order PDF
			# send order via email
			return redirect("cart:success")

	context = {
			"object":order_obj, 
			"billing_profile":billing_profile, 
			"login_form": login_form,
			"guest_form": guest_form,
			"address_form":address_form,
			"address_qs":address_qs
			}

	return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
	context={
	"order_number":request.session.get("order_number", None),
	"order_email":request.session.get("order_email", None)
	}
	return render(request, "carts/checkout-done.html", context)