from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse    
from .models import BinaryImage
from PIL import Image
import io
import os

def index(request):
    static_images = []
    media_images = BinaryImage.objects.all().order_by('-uploaded_at')
    image_folder = os.path.join(settings.BASE_DIR, 'static', 'images')
    for image_name in os.listdir(image_folder):
        static_images.append(os.path.join('images', image_name))
    return render(request, 'index.html', {'static_images': static_images, 'media_images': media_images})


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        img = Image.open(image_file)

        binary_image = img.convert("1")

        image_io = io.BytesIO()
        binary_image.save(image_io, format="PNG")
        image_io.seek(0)

        binary_image_instance = BinaryImage()
        binary_image_instance.image.save(image_file.name, image_io)
        binary_image_instance.save()

        image_url = binary_image_instance.image.url
        return JsonResponse({"success": True, "message": "Image uploaded successfully."})

    return JsonResponse({"success": False, "error": "No image uploaded."})
