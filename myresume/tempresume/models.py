from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.


class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Experience(models.Model):
    CV = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="experience")
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = RichTextField()

    def __str__(self):
        return self.company

class Education(models.Model):
    CV = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="education")
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    institution = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=100)
    description = RichTextField()

    def __str__(self):
        return self.institution


class Clause(models.Model):
    CV = models.ForeignKey(CV, on_delete=models.CASCADE)
    description = RichTextField()
    
    def __str__(self):
        return self.description[0:40]