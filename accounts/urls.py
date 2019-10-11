from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('logout/', views.user_logout, name = 'logout'),
        path('index/', views.index, name = 'index'),
        path('register/', views.register, name = 'register'),
        path('login/', views.user_login, name = 'login'),
        path('home/', views.home, name = 'home'),

]
