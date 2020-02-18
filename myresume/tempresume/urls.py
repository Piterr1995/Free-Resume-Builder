from django.urls import path
from . import views

app_name = "tempresume"

urlpatterns = [
    path('', views.index, name="index"),
    path('experience/', views.experience, name="experience")
]