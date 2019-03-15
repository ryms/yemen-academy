#from django.views import ListView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


from .models import Product

from carts.models import Cart



class ProductFeaturedListView(ListView):
	template_name = "products/views/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()

class ProductFeaturedDetailsView(DetailView):
	queryset = Product.objects.all().featured()
	template_name = "products/views/featured-detail.html"

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()


class ProductListView(ListView):
	queryset = Product.objects.all()
	template_name = "products/views/list.html"


	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		return context

def product_list_view(request):
	queryset = Product.objects.all()
	context = {'object_list':queryset}
	return render(request, "products/views/list.html", context)

class ProductSlugDetailsView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/views/details.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductSlugDetailsView, self).get_context_data(*args, **kwargs)
		cart_obj,new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		
		context['product_in_cart'] = cart_obj.cart_items.filter(Q(product__id__iexact=context['object'].id))
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get("slug")
		
		try:
			instance = Product.objects.get(slug = slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Product doesn't exists")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug = slug, active=True)
			instance = qs.first()
		except:
			raise Http404("Undefined error")
			
		return instance


class ProductDetailsView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/views/details.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailsView, self).get_context_data(*args, **kwargs)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get("pk")
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product doesn't exists")
		return instance

def product_details_view(request, pk=None, *args, **kwargs):
	#instance = Product.objects.get(pk=pk)
	#instance = get_object_or_404(Product, pk=pk)
	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product doesn't exists")

	# print(instance)

	# qs = Product.objects.filter(id=pk)
	# if qs.exists() and qs.count() == 1:
	# 	instance = qs.first()
	# else:
	# 	raise Http404("Product doesn't exists")

	# try:
	# 	instance = Product.objects.get(id=pk)
	# except Product.DoesNotExist:
	# 	raise Http404("Product doesn't exist")

	context = {'object':instance}
	return render(request, "products/views/details.html", context)