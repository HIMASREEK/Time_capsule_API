"""
URL configuration for time_capsule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from accounts.views import login_page
from capsules.views import create_capsule_page, delete_capsule, edit_capsule
from capsules.views import dashboard
from django.conf import settings
from django.conf.urls.static import static
from capsules.views import (
    dashboard, create_capsule_page,
    delete_capsule, edit_capsule, share_capsule
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='home'),

    path('create/', create_capsule_page),
    path('dashboard/', dashboard, name='dashboard'),

    path('share/<uuid:token>/', share_capsule, name='share'),
    path('delete/<int:id>/', delete_capsule),
    path('edit/<int:id>/', edit_capsule),   # 👈 ADD THIS

    path('api/auth/', include('accounts.urls')),
    path('api/capsules/', include('capsules.urls')),
    path('api/auth/', include('accounts.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)