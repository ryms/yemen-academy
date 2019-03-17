from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart,ProductInCart
from billing.models import BillingProfile
from accounts.views import LoginForm

from orders.models import Order

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
	if cart_created or cart_obj.cart_items.count() == 0:
		redirect("cart:home")
	else:
		order_obj, new_order_obj = Order.objects.get_or_create(cart = cart_obj)

	billing_profile = None
	user = request.user
	if user.is_authenticated:
		billing_profile,billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)

	loginForm = LoginForm()

	context = {"object":order_obj, "billing_profile":billing_profile, "loginForm": loginForm}

	return render(request, "carts/checkout.html", context)