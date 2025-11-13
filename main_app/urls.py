from django.urls import path
from . import views

urlpatterns = [
    path('',views.page, name="page"),
    path('process',views.process,name="process"),
      path('chatbot/', views.chatbot, name='chatbot'),
]