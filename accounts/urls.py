from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_api),
    path('login/', login_api),

    path('register-page/', register_page, name='register'),
    path('', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
]