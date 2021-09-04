from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index), 
    path('administrador/', views.administrador),
    path('wall/', auth.wall),
    path('post_message', auth.post_message), 
    path('add_comment', auth.add_comment), 
    path('registro/', auth.registro),
    path('login/', auth.login),
    path('logout/', auth.logout)
]
