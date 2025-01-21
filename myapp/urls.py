from django.urls import path
from .views import upload_image
from .views import login_page
from django.urls import path, include

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', login_page, name='login_page'),
]