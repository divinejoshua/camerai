from django.shortcuts import render
from django.views.generic import TemplateView

from .models import OrginalImage
from .forms import CreateImageForm

# OpenAI 

# Settings 
import requests
from django.conf import settings


# Create your views here.
class HomeView(TemplateView):
    template_name = "camerai/index.html"
    context = {}

    # Get request 
    def get(self, request, *args, **kwargs):
        print(request.META['HTTP_HOST'])
        return render(request, self.template_name)

    # Post request 
    def post(self, request, *args, **kwargs):

        # Create form instance 
        form = CreateImageForm(request.POST or None, request.FILES or None)

        # Save form data
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            self.context['orginal_image'] = obj.image

            image_url = 'http://'+request.META['HTTP_HOST']+'/media/'+str(obj.image)

            # call the generate method 
            self.generateImage(image_url)


            form = CreateImageForm()

        self.context['form'] = form

        return render(request, self.template_name, self.context)

    
    
    # Stability AI image generation
    def generateImage(self, image_url, *args, **kwargs):  
        headers = {
            'Authorization': settings.HOTPOT_AI_KEY,
        }

        # change to a full file path of the image you want to transform
        body = {
            'image': open('didi.jpg', 'rb'),
        }

        response = requests.post('https://api.hotpot.ai/stable-diffusion-normal', headers=headers, files=body)

        # change to a full file path where you want to save the resulting image
        with open('image.jpg', 'wb') as file:
            file.write(response.content)
        
        print("hi")



