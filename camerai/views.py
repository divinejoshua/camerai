from django.shortcuts import render
from django.views.generic import TemplateView

from .models import OrginalImage
from .forms import CreateImageForm

# OpenAI 

# Settings 
from django.conf import settings


import io
import os
import warnings

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation



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

        # Set up our connection to the API.
        stability_api = client.StabilityInference(
            key=settings.STABILITY_KEY, # API Key reference.
            verbose=True, # Print debug messages.
            engine="stable-diffusion-v1-5", # Set the engine to use for generation. For SD 2.0 use "stable-diffusion-v2-0".
            # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
            # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
        )

        # Set up our initial generation parameters.
        answers = stability_api.generate(
            prompt="a rocket-ship launching from rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli",
            seed=892226758, # If a seed is provided, the resulting generated image will be deterministic.
                            # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                            # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
            steps=30, # Amount of inference steps performed on image generation. Defaults to 30.
            cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                        # Setting this value higher increases the strength in which it tries to match your prompt.
                        # Defaults to 7.0 if not specified.
            width=512, # Generation width, defaults to 512 if not included.
            height=512, # Generation height, defaults to 512 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
        )

        # Set up our warning to print to the console if the adult content classifier is tripped.
        # If adult content classifier is not tripped, display generated image.
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    global img
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save(str(artifact.seed)+ ".png") # Save our generated images its seed number as the filename.



