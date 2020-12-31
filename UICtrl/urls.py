from django.contrib import admin
from django.urls import path,include
from UICtrl import views
urlpatterns = [
    path('',views.home),
    path('login',views.loginn),
     path('signup',views.signup),
    path('logout',views.Logout),

]