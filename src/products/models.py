import os
import random
from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator

from django.urls import reverse

def get_filename_ext(filename):
	base_name = os.path.basename(filename)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1, 3000000220)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext = ext)
	return "products/{new_filename}/{final_filename}".format(
			new_filename=new_filename, final_filename=final_filename
		)

class PrdocutQuerySet(models.query.QuerySet):
	def featured(self):
		return self.filter(featured = True, active = True)

	def active(self):
		return self.filter(active = True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return PrdocutQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		else:
			return None

	def featured(self):
		return self.get_queryset().featured()

class Product(models.Model):
	title 		= models.CharField(max_length=120)
	slug		= models.SlugField(blank=True, unique=True)
	description = models.TextField()
	price 		= models.DecimalField(decimal_places = 2, max_digits=20, default=0.00)
	image 		= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	featured	= models.BooleanField(default=False)
	active		= models.BooleanField(default=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = ProductManager()

	def get_absolute_url(self):
		return reverse("products:detail", kwargs={"slug":self.slug})

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance, instance.title)

pre_save.connect(product_pre_save_receiver, sender=Product)
