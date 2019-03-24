from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
	('billing', 'Billing'),
	('shipping', 'Shipping')
	)
class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, models.PROTECT)
	address_type	= models.CharField(max_length = 120, choices=ADDRESS_TYPES)
	address_line_1 	= models.CharField(max_length=250)
	address_line_2 	= models.CharField(max_length=250)
	country			= models.CharField(max_length = 120)
	city			= models.CharField(max_length = 120)
	state			= models.CharField(max_length = 120)
	post_code		= models.CharField(max_length = 120)


	def __str__(self):
		return str(self.billing_profile)

	def get_address(self):

		return "{line1}, {line2} \n {country} \n{city} \n{post_code} \n {state} \n".format(
			line1=self.address_line_1 or "", 
			line2=self.address_line_2 or "",
			country=self.country or "",
			city=self.city or "",
			post_code=self.post_code or "",
			state=self.state or ""
			)
