from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('barcode/api/fonts/encode/base64', views.encodeFont, name='encode')
]