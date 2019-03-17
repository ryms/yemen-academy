
def generate_order_id(instance, prefix, size=10):
	klass = instance.__class__

	last_order = klass.objects.all().order_by("-id").first()
	last_order_id = 1
	if last_order is not None:
		last_order_id = last_order.id + 1

	return "{prefix}_{order_id:0{size}d}".format(prefix=prefix, order_id=last_order_id, size= size)




