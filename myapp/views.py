from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import Image
from django.http import JsonResponse
from bson import Binary
from .utils import db
from datetime import datetime
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def login_page(request):
    return render(request, 'account/login.html')  # 'login.html' es el archivo HTML creado arriba.




@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        image_data = image_file.read()
        image_name = image_file.name

       

        # Guardar la imagen en MongoDB
        db.imagenes.insert_one({
            'name': image_name,
            'data': Binary(image_data),
            'content_type': image_file.content_type,
            'uploaded_by':  User.objects.first().email,
            'timestamp': datetime.now(),
        })

        return JsonResponse({'message': 'Imagen subida exitosamente', 'email': User.objects.first().email})

    return render(request, 'upload_image.html')