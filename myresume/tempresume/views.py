from django.shortcuts import render, redirect
from .forms import PersonalInfoForm, ExperienceForm
from django.http import HttpResponse, HttpResponseRedirect
from redis import StrictRedis
from django.conf import settings
from django.contrib import messages
import json

# Create your views here

r = StrictRedis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def index(request):
    exp_forms = []
    if request.method == "POST":
        form = PersonalInfoForm(request.POST)
        # form1 = ExperienceForm(request.POST)
        # form2 = ExperienceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = str(form.cleaned_data['date_of_birth'])
            address = str(form.cleaned_data['address'])
            postal_code = form.cleaned_data['postal_code']
            city = form.cleaned_data['city']
            # exp_1_company = form1.cleaned_data['company']
            # exp_2_company = form2.cleaned_data['company']
            data = {'name': name, 
                    'last_name': last_name, 
                    'date_of_birth': date_of_birth,
                    'address': address,
                    'postal_code': postal_code,
                    'city': city}
            rdict = json.dumps(data)
            r.set(f'{date_of_birth}', rdict)
            r.expire(f'{date_of_birth}', 120)
            
            data_from_redis = r.get(f'{date_of_birth}')
            results = json.loads(data_from_redis)

            print(results)
            return redirect('www.fcbarca.com')
    else:
        print("witam")
        form = PersonalInfoForm()
        # form1 = ExperienceForm()
        # form2 = ExperienceForm()
        
        
    return render(request, 'tempresume/index.html', {'form': form,})


    
