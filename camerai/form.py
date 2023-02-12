from django import forms

from .models import OrginalImage 


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = OrginalImage
		fields = ['image']