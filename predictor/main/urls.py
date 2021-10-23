from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    #path('', views.textbox, name='textbox'),
    path('generate',views.generate,name='generate'),
    
]