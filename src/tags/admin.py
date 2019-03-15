from django.contrib import admin

from .models import Tag

class TagAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug', 'active']
	class Meta:
		model = Tag

admin.site.register(Tag)
