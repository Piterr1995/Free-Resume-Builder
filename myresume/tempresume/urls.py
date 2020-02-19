from django.urls import path
from . import views

app_name = "tempresume"

urlpatterns = [
    path('', views.index, name="index"),
    path('generated_cv/<slug:r_CV_name>/<slug:r_date_of_birth>', views.generate_pdf, name="generate_pdf"),
]