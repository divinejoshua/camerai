from django.shortcuts import render
from django.views.generic import TemplateView

from .models import OrginalImage
from .forms import CreateImageForm

# OpenAI 
import openai
import urllib.request, urllib.parse, urllib.error

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

        # Get data from image url

        img = urllib.request.urlopen(image_url).read()
        fhand = open('cover3.jpg', 'wb')
        fhand.write(img)
        fhand.close()

        # Send request to open AI image generation
        response = openai.Image.create_edit(
            image=open("cover3.jpg", "rb"),
            mask=open("mask.png", "rb"),
            prompt="A sunlit indoor lounge area with a pool containing a flamingo",
            n=1,
            size="1024x1024"
        )
        # recieve response url
        new_image_url = response['data'][0]['url']

        print(new_image_url)
        return 


