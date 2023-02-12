from django.contrib import admin

from .models import OrginalImage, GenertedImages

# Models 
admin.site.register(OrginalImage)
admin.site.register(GenertedImages)