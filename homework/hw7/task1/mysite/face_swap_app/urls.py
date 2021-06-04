from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'face_swap_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('image_upload', views.image_view, name='image_upload'),
    path('success', views.success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
