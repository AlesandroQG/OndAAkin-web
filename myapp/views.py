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
import base64


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
    
def image_list(request):
    images = db.imagenes.find({}, {'name': 1, '_id': 1})  # Solo obtenemos el nombre y el ID
    image_data = [{'id': str(image['_id']), 'name': image['name']} for image in images]
    return JsonResponse({'images': image_data})

def get_image(request, image_id):
    image = db.imagenes.find_one({'_id': ObjectId(image_id)})
    
    if image:
        # Convierte los datos binarios a base64 para servirlos
        base64_data = base64.b64encode(image['data']).decode('utf-8')
        return HttpResponse(f"data:{image['content_type']};base64,{base64_data}", content_type="text/html")
    
    return HttpResponse("Imagen no encontrada", status=404)
    
def display_images(request):
    # Obtén todas las imágenes de MongoDB
    images = db.imagenes.find()
    
    # Construye la lista de imágenes en formato base64 para enviarlas a la plantilla
    image_data = []
    for image in images:
        image_id = str(image['_id'])
        base64_data = base64.b64encode(image['data']).decode('utf-8')
        image_data.append({
            'id': image_id,
            'name': image['name'],
            'base64_data': base64_data,
            'content_type': image['content_type']
        })
    
    return render(request, 'display_images.html', {'images': image_data})