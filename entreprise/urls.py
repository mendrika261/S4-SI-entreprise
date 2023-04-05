"""
URL configuration for entreprise project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from comptable.views import user_view
from comptable.views import global_view
from entreprise import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='home'),
    path('', include('comptable.urls')),

    path('connexion', user_view.login_view, name='login'),
    path('deconnexion', user_view.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = global_view.custom_404_view
