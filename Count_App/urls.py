from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home page that displays the login view
    path('', views.login, name='login'),
    # Login page for users  
    path('login', views.login, name='login'), 
    # User registration page
    path('registration', views.registration, name='registration'),  
    # Page for uploading data
    path('upload_data', views.upload_data, name='upload_data'), 
    # View for listing users
    path('users', views.users, name='users'),  
    # API endpoint for querying data
    path('query_builder', views.query_builder, name='query_builder'), 
    # Logout functionality 
    path('logout', views.logout, name='logout'),  

    
]