from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_capsule),
    path('list/', get_capsules),
    path('open/<int:id>/', open_capsule),

    # frontend
    path('dashboard/', dashboard, name='dashboard'),
    path('create-page/', create_capsule_page),
    path('delete/<int:id>/', delete_capsule),
]