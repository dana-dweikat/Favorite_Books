from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'app1'

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('add_book', views.add_book, name='add_book'),
    path('book/<int:pk>', views.book, name='book'),
    path('add_to_favorite/<int:pk>', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<int:pk>', views.remove_from_favorite, name='remove_from_favorite'),
    path('update/<int:pk>', views.updated, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),

]

