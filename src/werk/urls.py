from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.homeView, name="werk-home"),
    path('login', views.loginView, name="werk-login"),
    path('cadastro', views.cadastroView, name="werk-cadastro"),
]