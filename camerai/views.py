from django.shortcuts import render
from django.views.generic import TemplateView

from .models import OrginalImage
from .forms import CreateImageForm


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
            print('http://'+request.META['HTTP_HOST']+'/media/'+str(obj.image))
            form = CreateImageForm()

        self.context['form'] = form

        return render(request, self.template_name, self.context)

    # Open AI image generation
    def generateImage(self, image_url, *args, **kwargs):
        response = openai.Image.create_edit(
            image=open("sunlit_lounge.png", "rb"),
            mask=open("mask.png", "rb"),
            prompt="A sunlit indoor lounge area with a pool containing a flamingo",
            n=1,
            size="1024x1024"
        )
        new_image_url = response['data'][0]['url']
        return new_image_url


