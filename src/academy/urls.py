"""academy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

# from products.views import (
# 	ProductListView, 
# 	product_list_view, 
# 	ProductDetailsView, 
# 	product_details_view,
# 	ProductFeaturedListView,
# 	ProductFeaturedDetailsView,
# 	ProductSlugDetailsView
# 	)

from .views import home_page,about_page,contact_page,login_page,register_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page , name="home"),
    path('index', home_page, name="index"),
    path('about', about_page, name="about"),
    path('contact', contact_page, name="contact"),
    path('products/', include(("products.urls", "products"), namespace="products")),
    
    path('bootstarp', TemplateView.as_view(template_name="bootstrap/example.html")),
    

    # path('products', ProductListView.as_view()),
    # path('products-abc', product_list_view),
    # path('products/<int:pk>/', ProductDetailsView.as_view()),
    # path('products-abc/<int:pk>/', product_details_view),
    # url('^products/(?P<pk>\d+)/$', ProductDetailsView.as_view()),
    # url('^products-abc/(?P<pk>\d+)/$', product_details_view),
    # path('products/<slug:slug>/', ProductSlugDetailsView.as_view()),

    #path('featured', ProductFeaturedListView.as_view()),
    #path('featured/<int:pk>/', ProductFeaturedDetailsView.as_view()),
    
    
    path('login', login_page, name="login"),
    path('register', register_page, name="register"),
]

if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
