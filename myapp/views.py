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
import json
import os
from .segment import segment_image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def upload_image_and_segment(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        # Procesar la imagen con la segmentación
        image_segmented=segment_image(image.read())
        response=JsonResponse({'status': 'success', 'base64_string': image_segmented})
        print(response.status)
        print(response.base64_string)
        return response
    return render(request, "upload_image_and_segment.html")

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


def get_annotations(request):
    return render(request, 'via.html') 
    
@csrf_exempt
def save_annotations(request):
    if request.method == 'POST':
        try:
            # Obtén los datos JSON del cuerpo de la solicitud
            datos = json.loads(request.body)
            
            # Inserta los datos en MongoDB
            resultado = db.annotations.insert_one(remove_dots_from_keys(datos))

            # Devuelve una respuesta de éxito
            return JsonResponse({'mensaje': 'Datos guardados correctamente', 'id': str(resultado.inserted_id)})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            print('Error inesperado:', e)
            return JsonResponse({'error': f'Ocurrió un error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
        
def remove_dots_from_keys(data):
    if isinstance(data, dict):
        # Crea un nuevo diccionario con claves sin puntos
        return {key.replace('.', '_'): remove_dots_from_keys(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Aplica la función recursivamente a cada elemento si es una lista
        return [remove_dots_from_keys(item) for item in data]
    else:
        # Devuelve el valor tal cual si no es un dict ni una lista
        return data
