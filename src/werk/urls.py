from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.homeView, name="werk-home"),
    path('login', views.loginView, name="werk-login"),
    path('logout', views.logoutUser, name="werk-logout"),
    path('cadastro', views.cadastroView, name="werk-cadastro"),
    path('addTask', views.addTask),
    path('<id>/delete', views.removeTask, name="removeTask"),
    path('<id>/start', views.startTask, name="startTask"),
    path('<id>/end', views.finishTask, name="finishTask"),
]