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
    if request.method == "POST":
        personal_info_form = PersonalInfoForm(request.POST)
        exp_1_form = exp_2_form = exp_3_form = exp_4_form = exp_5_form = exp_6_form = exp_7_form = exp_8_form = exp_9_form = exp_10_form = ExperienceForm(request.POST)
        exp_forms = [exp_1_form, exp_2_form, exp_3_form, exp_4_form, exp_5_form, exp_6_form, exp_7_form, exp_8_form, exp_9_form, exp_10_form]
        if personal_info_form.is_valid() and [form.is_valid() for form in exp_forms]:

            #Personal Info
            name = personal_info_form.cleaned_data['first_name']
            last_name = personal_info_form.cleaned_data['last_name']
            date_of_birth = str(personal_info_form.cleaned_data['date_of_birth'])
            address = str(personal_info_form.cleaned_data['address'])
            postal_code = personal_info_form.cleaned_data['postal_code']
            city = personal_info_form.cleaned_data['city']

            #Experience
            # exp1_form = exp2_form = exp3_form = exp4_form = exp5_form = exp6_form = exp7_form = exp8_form = exp9_form = exp10_form = ExperienceForm(request.POST)
            # exp_forms = [exp1_form, exp2_form, exp3_form, exp4_form, exp5_form, exp6_form, exp7_form, exp8_form, exp9_form, exp10_form]
            
            # exp_1_company = form1.cleaned_data['company']
            # exp_2_company = form2.cleaned_data['company']
            data = {'Personal_info': {'name': name, 
                                    'last_name': last_name, 
                                    'date_of_birth': date_of_birth,
                                    'address': address,
                                    'postal_code': postal_code,
                                    'city': city}
            }

            data["Experience"] = {}
            # data['Experience']['1'] = {'company': exp_1_form.cleaned_data['company'],
            #                             'start_date': str(exp_1_form.cleaned_data['start_date']),
            #                             'end_date': str(exp_1_form.cleaned_data['end_date']),
            #                             }
            # data['Experience']['2'] = {'company': exp_2_form.cleaned_data['company'],
            #                             'start_date': str(exp_2_form.cleaned_data['start_date']),
            #                             'end_date': str(exp_2_form.cleaned_data['end_date']),
            #                             }
            for index, exp_form in enumerate(exp_forms):
                if exp_form.cleaned_data['company']:
                    company = exp_form.cleaned_data['company']
                else:
                    company = None
                data['Experience'][f'{index}'] = {'company': str(company),
                                                'start_date': str(exp_form.cleaned_data['start_date']),
                                                'end_date': str(exp_form.cleaned_data['end_date']),
                                            # 'description': exp_form.cleaned_data['description'],
                                            }
                    
            
            print(data)
            
            rdict = json.dumps(data)
            r.set(f'{date_of_birth}', rdict)
            r.expire(f'{date_of_birth}', 120)
            
            data_from_redis = r.get(f'{date_of_birth}')
            results = json.loads(data_from_redis)

            print(results)
            return redirect('www.fcbarca.com')
    else:
        print("witam")
        personal_info_form = PersonalInfoForm()
        exp1_form = exp2_form = exp3_form = exp4_form = exp5_form = exp6_form = exp7_form = exp8_form = exp9_form = exp10_form = ExperienceForm()
        exp_forms = [exp1_form, exp2_form, exp3_form, exp4_form, exp5_form, exp6_form, exp7_form, exp8_form, exp9_form, exp10_form]
        # exp_1_form = ExperienceForm()
        # exp_2_form = ExperienceForm()
        
    return render(request, 'tempresume/index.html', {'personal_info_form': personal_info_form, 'exp_forms': exp_forms})


    
