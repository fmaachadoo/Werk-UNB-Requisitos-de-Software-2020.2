from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="werk-home"),
    path('login', views.login, name="werk-login"),
]