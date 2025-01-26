# **OndAAkin-web**

OndAAkin-web es una aplicación basada en Django para gestionar y segmentar imágenes de manera eficiente. Este proyecto permite a los usuarios anotar imágenes manualmente y procesarlas mediante un modelo avanzado de segmentación de imágenes.

---

## **Requisitos Previos**

Asegúrate de que tienes las siguientes herramientas y librerías instaladas antes de ejecutar el proyecto:

- **Python 3.10**
- **Django**
- **django-allauth**
- **requests**
- **jwt**
- **bson**
- **pymongo**
- **samv2**

---

## **Configuración del Entorno**

### **1. Configurar MongoDB con Docker**  
Descarga e inicia un contenedor de MongoDB con los siguientes comandos:  

```bash
docker pull mongo
docker run --name some-mongo -d mongo:tag
2. Clonar el Repositorio
Navega a tu directorio de trabajo y clona el proyecto.


git clone <URL-del-repositorio>
cd myproject
3. Ejecutar el Servidor de Django
Inicia el servidor local de Django:


python manage.py runserver 0.0.0.0:8000
4. Acceso a la Aplicación
Página de inicio de sesión:
http://localhost:8000/accounts/login/
Galería de imágenes:
http://localhost:8000/accounts/allimages/
Características Principales
1. Anotación Manual de Imágenes
Accede al módulo de anotaciones en:
http://localhost:8000/annotations/

Anota imágenes manualmente utilizando las herramientas proporcionadas.
Para guardar las anotaciones, utiliza el botón "Exportar" y genera un archivo JSON.
2. Segmentación Automática de Imágenes
Sube imágenes y procesa su segmentación automáticamente en:
http://localhost:8000/upload_image_and_segment/

La imagen será segmentada utilizando el modelo SAM2.
Una vez procesada, podrás visualizar la imagen segmentada y guardar los resultados.
Documentación Técnica
Requisitos de Librerías
Instala las dependencias necesarias mediante pip:


pip install django django-allauth requests jwt bson pymongo samv2
Rutas Principales
Ruta	Descripción
/accounts/login/	Página de inicio de sesión.
/accounts/allimages/	Galería de imágenes cargadas.
/annotations/	Módulo para anotar imágenes manualmente.
/upload_image_and_segment/	Subir y segmentar imágenes automáticamente.
Uso
Inicia MongoDB
Asegúrate de que tu contenedor de MongoDB está en ejecución:


docker start some-mongo
Inicia el servidor de Django
Ejecuta el comando:


python manage.py runserver
Accede a la aplicación
Usa las rutas mencionadas en la sección de Rutas Principales para interactuar con las funcionalidades.

