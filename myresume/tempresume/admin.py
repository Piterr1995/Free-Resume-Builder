from django.contrib import admin
from .models import CV, Experience, Education, Clause

# Register your models here.

class ExperienceInlines(admin.TabularInline):
    model = Experience
    extra = 0
    fields = ['start_date', 'end_date', 'company', 'position', 'description']

class EducationInlines(admin.TabularInline):
    model = Education
    extra = 0
    fields = ['start_date', 'end_date', 'institution', 'specialisation', 'description']
    
class ClauseInline(admin.TabularInline):
    model = Clause
    extra = 0
    fields = ['description',]

@admin.register(CV)
class CV_Admin(admin.ModelAdmin):
    fields = ['name',]
    inlines = [ExperienceInlines, EducationInlines, ClauseInline]
