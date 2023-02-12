from django import forms

from .models import OrginalImage 


class CreateImageForm(forms.ModelForm):

	class Meta:
		model = OrginalImage
		fields = ['image']