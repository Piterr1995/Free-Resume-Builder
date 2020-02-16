from django.shortcuts import render, redirect
from .forms import PersonalInfoForm, ExperienceForm
from django.http import HttpResponse, HttpResponseRedirect
from redis import StrictRedis
from django.conf import settings

# Create your views here

r = StrictRedis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def index(request):
    exp_forms = []
    if request.method == "POST":
        form = PersonalInfoForm(request.POST)
        form1 = ExperienceForm(request.POST)
        form2 = ExperienceForm(request.POST)

        if form.is_valid() and form1.is_valid() and form2.is_valid():
            name = form.cleaned_data['first_name']
            exp_1_company = form1.cleaned_data['company']
            exp_2_company = form2.cleaned_data['company']
            print(name, exp_1_company, exp_2_company)
            return redirect('www.fcbarca.com')
    else:
        print("witam")
        form = PersonalInfoForm()
        form1 = ExperienceForm()
        form2 = ExperienceForm()
        exp_forms = [form1, form2]
        
    return render(request, 'tempresume/index.html', {'form': form, 'exp_forms': exp_forms})

def personal_info(request):
    
