from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.homeView, name="werk-home"),
    path('login', views.loginView, name="werk-login"),
    path('logout', views.logoutUser, name="werk-logout"),
    path('cadastro', views.cadastroView, name="werk-cadastro"),
    path('profile', views.profileView, name="werk-profile"),
    path('dashboard', views.dashboardView, name="dashboard")
]