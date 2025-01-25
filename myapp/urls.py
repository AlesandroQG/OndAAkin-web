from django.urls import path
from .views import upload_image
from .views import login_page
from .views import *
from django.urls import path, include

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', login_page, name='login_page'),
    path('annotations/', get_annotations, name='get_annotations'),
    path('save_annotations/', save_annotations, name='save_annotations'),
]