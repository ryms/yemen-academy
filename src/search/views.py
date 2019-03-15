from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product

class SearchProductView(ListView):
	template_name = "search/view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_data(*args, **kwargs)
		query = self.request.GET.get('q', None)
		context['query'] = query

		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		query = request.GET.get('q', None)
		if query is not None and query is not '':
			return Product.objects.search(query)
		else:
			return Product.objects.featured()


		'''
		__icontains = field contains this
		__iexact = field is exactly this
		'''