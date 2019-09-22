from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from facegram import views

urlpatterns = [
    path('',include('facegram.urls')),
    path('admin/', admin.site.urls),
    path('facegram/', include('facegram.urls')),
    path('auth/password_change/done /',include('facegram.urls')),
    path('auth/', include('django.contrib.auth.urls')),
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

