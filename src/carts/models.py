from decimal import Decimal
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, m2m_changed 
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL

class ProductInCart(models.Model):
	session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
	product   = models.ForeignKey(Product, null=True, blank=True, on_delete=models.PROTECT)
	count_item = models.IntegerField(default=1)
	price_per_item = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	total_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	is_active = models.BooleanField(default=True)
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	def __str__(self):
		if self.product is not None:
			return self.product.name
		else:
			return self.id

	class Meta:
		verbose_name = 'Product in basket'
		verbose_name_plural = 'Product in basket'

	def save(self, *args, **kwargs):
		self.price_per_item = self.product.price
		self.total_price = self.count_item * self.price_per_item
		super(ProductInCart, self).save(*args, **kwargs)

class CartManager(models.Manager):
	def new_or_get(self, requset):
		cart_id = requset.session.get('cart_id', None)
		qs = Cart.objects.filter(id=cart_id)
		if qs.count() == 1:
			new_obj = False
			cart_obj = qs.first()
			if requset.user.is_authenticated and cart_obj.user is None:
				cart_obj.user = requset.user
				cart_obj.save()
		else:
			cart_obj = Cart.objects.new(user = requset.user)
			new_obj = True
			requset.session['cart_id'] = cart_obj.id
		return cart_obj, new_obj

	def new(self, user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)

	def update(self, request, product_obj, count, action):
		cart_obj, new_obj = self.new_or_get(request)
		cart_items = cart_obj.cart_items.all()

		product_in_cart = None
		product_in_cart = cart_obj.cart_items.filter(Q(product__id__iexact=product_obj.id)).first()

		if product_in_cart is not None:
			if action == "delete":
				cart_obj.cart_items.remove(product_in_cart)
			elif action == "add":
				product_in_cart.count_item +=1
				product_in_cart.save()
			elif action == "update":
				if count == 0:
					cart_obj.cart_items.remove(product_in_cart)
				else:
					product_in_cart.count_item = count
					product_in_cart.save()
			
		else:
			product_in_cart = ProductInCart.objects.create(product = product_obj)
			product_in_cart.save()
			cart_obj.cart_items.add(product_in_cart)

		cart_obj.update_cart()


class Cart(models.Model):
	user 	  = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
	cart_items= models.ManyToManyField(ProductInCart, blank = True)
	subtotal  = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	total 	  = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	count_items = models.IntegerField(default=0)
	updated	  = models.DateTimeField(auto_now = True)
	timestamp = models.DateTimeField(auto_now_add = True)

	objects   = CartManager()

	def update_cart(self):
		productsInCart = self.cart_items.all()
		total = 0
		count = 0
		for prodInCart in productsInCart:
			total +=prodInCart.total_price
			count +=prodInCart.count_item

		self.subtotal = total
		self.count_items = count
		self.save()

	def __str__(self):
		return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
	if action in ['post_add', 'post_remove', 'post_clear']:
		instance.update_cart()

m2m_changed.connect(m2m_changed_cart_receiver, sender = Cart.cart_items.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
	if instance.subtotal > 0:
		instance.total = Decimal(instance.subtotal) * Decimal(1.08) # tax
	else:
		instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender = Cart)


