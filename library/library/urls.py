"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from decorator_include import decorator_include
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.views import LoginView

def check_user(user):
    return user.is_superuser()

urlpatterns = [

    path('index/login/', LoginView.as_view(template_name='login.html'), name="login"),

    path('admin/docs/', decorator_include(user_passes_test(lambda u: u.is_superuser), 'django.contrib.admindocs.urls')),

    path('admin/', admin.site.urls),

    path('index/', include('django.contrib.auth.urls')),

    path('', include('barcode.urls')),
]