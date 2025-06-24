"""
URL configuration for TumorGANProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from TumorGAN.views import index,about,treatment,tumor_analysis,result,login_view, user_logout

urlpatterns = [
    path('', login_view, name='login_view'),
        path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('treatment/', treatment, name='treatment'),
    path('tumor-analysis/', tumor_analysis, name='tumor_analysis'),
    path('result/', result, name='result'),
    path('logout/', user_logout, name='logout'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)