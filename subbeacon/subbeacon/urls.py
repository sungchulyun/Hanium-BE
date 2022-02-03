"""subbeacon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import routers
from restapi_beacon import views
from subbeacon  import settings
from django.conf.urls.static import static
from restapi_beacon.models import ocrimg

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'subways', views.subwayViewSet)
router.register(r'arrival', views.arrivalViewSet)
router.register(r'destination', views.destinationViewSet)
router.register(r'subwayim', views.subwayimViewSet)
router.register(r'destination', views.destinationViewSet)
router.register(r'userstatus', views.userstatusViewSet)
router.register(r'naviroot', views.navirootViewSet)
router.register(r'ocrimg', views.ocrimgViewSet)

urlpatterns = [
    path('restapi_beacon/', include('restapi_beacon.urls')),
    path('', include(router.urls)),
    re_path('admin/', admin.site.urls),
    re_path(r'^$', views.IndexView.as_view(), name='index'),


]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
