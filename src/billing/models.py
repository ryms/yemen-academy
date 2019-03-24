from django.db import models
from django.db.models.signals import post_save

from django.conf import settings

from accounts.models import GuestEmail


User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		user = request.user
		guest_email_id = request.session.get('guest_email_id')

		billing_profile = None
		obj=None

		created = False
	
		if user.is_authenticated:
			'logged in user checkout; remember payment stuff'
			obj,created = self.model.objects.get_or_create(user=user,email=user.email)
		elif guest_email_id is not None:
			'guest user checkout; auto reloads payment stuff'
			guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
			obj,created = self.model.objects.get_or_create(email=guest_email_obj.email)

		else:
			pass
		return obj,created


class BillingProfile(models.Model):
	user 	 = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)
	email 	 = models.EmailField()
	active	 = models.BooleanField(default=True)
	update	 = models.DateTimeField(auto_now=True)
	timestamp= models.DateTimeField(auto_now_add=True)

	#customer_id in Stripe or BrainTree

	objects=BillingProfileManager()

	def __str__(self):
		return self.email


# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		print("Actual API request send Stripe / BrainTree")
# 		instance.customer_id = newID
# 		instance.save()

def user_created_receiver(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects().get_or_create(user=instance, email=instance.email)

# pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)
post_save.connect(user_created_receiver, sender=User)