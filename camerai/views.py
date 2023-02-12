from django.shortcuts import render
from django.views.generic import TemplateView

from .models import OrginalImage
from .forms import CreateImageForm

# OpenAI 
import openai
import urllib.request, urllib.parse, urllib.error

# Settings 
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

    # Open AI image generation
    def generateImage(self, image_url, *args, **kwargs):

        # Set up open AI authorization
        openai.api_key = settings.OPENAI_API_KEY

        # Get data from image url

        # Write the image data to the file
        # img = urllib.request.urlopen(image_url).read()
        # fhand = open('image.png', 'wb')
        # fhand.write(img)
        # fhand.close()

        # Send request to open AI image generation
        response = openai.Image.create_variation(
            image=open("image.png", "rb"),
            n=1,
            size="1024x1024"
        )
        # recieve response url
        new_image_url = response['data'][0]['url']

        return 


