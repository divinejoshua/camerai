from django.db import models

# Create your models here.

def upload_location(instance, filename):
	file_path = 'images/{filename}'.format(
			filename=filename)
	return file_path

class OrginalImage(models.Model):
    image           = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published 	= models.DateTimeField(auto_now_add=True, verbose_name="date published")

class GenertedImages(models.Model):
    generatedImage  = models.ForeignKey(OrginalImage, on_delete=models.CASCADE)
    orginalImage    = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published 	= models.DateTimeField(auto_now_add=True, verbose_name="date published")