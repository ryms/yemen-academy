from django.urls import path

from .views import (
	ProductListView, 
	ProductSlugDetailsView
	)

urlpatterns = [
    path('', ProductListView.as_view(), name="list"),
    path('<slug:slug>', ProductSlugDetailsView.as_view(), name='detail'),
]

