from django.shortcuts import render, redirect
from .forms import PersonalInfoForm, ExperienceForm, EducationForm
from django.http import HttpResponse, HttpResponseRedirect
from redis import StrictRedis
from django.conf import settings
from django.contrib import messages
from django.forms import formset_factory
import json
from django.views.decorators.http import require_POST

# Create your views here

r = StrictRedis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def index(request):
    ExperienceFormset = formset_factory(ExperienceForm, extra=9)
    EducationFormset = formset_factory(EducationForm, extra=4)
    
    if request.method == "POST":
        #Personal info Form
        personal_info_form = PersonalInfoForm(request.POST)

        #Experience formset
        experience_formset = ExperienceFormset(request.POST, prefix='experience')
        
        #Education formsset
        education_formset = EducationFormset(request.POST, prefix='education')

        if personal_info_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid():

            #Personal Info
            CV_name = personal_info_form.cleaned_data['CV_name']
            first_name = personal_info_form.cleaned_data['first_name']
            last_name = personal_info_form.cleaned_data['last_name']
            date_of_birth = str(personal_info_form.cleaned_data['date_of_birth'])
            address = str(personal_info_form.cleaned_data['address'])
            postal_code = personal_info_form.cleaned_data['postal_code']
            city = personal_info_form.cleaned_data['city']

            data = {'Slug': str(CV_name + "/" + date_of_birth)
                    'Personal_info': {'first_name': first_name, 
                                    'last_name': last_name, 
                                    'date_of_birth': date_of_birth,
                                    'address': address,
                                    'postal_code': postal_code,
                                    'city': city}
            }


            # Experience
            data["Experience"] = {}

            for index, exp_form in enumerate(experience_formset):
                e = exp_form.cleaned_data
                # print(exp_form.cleaned_data.get('company'))
                if e.get('company'):
                    company = str(e.get('company'))
                else:
                    company = None
                if e.get('position'):
                    position = str(e.get('position'))
                else:
                    position = None
                if e.get('start_date'):
                    start_date = str(e.get('start_date'))
                else:
                    start_date = None
                if e.get('end_date'):
                    end_date = str(e.get('end_date'))
                else:
                    end_date = None

                data['Experience'][f'{index}'] = {'company': company,
                                                'position': position,
                                                'start_date': start_date,
                                                'end_date': end_date,
                                            # 'description': exp_form.cleaned_data['description'],
                                            }


            data['Education'] = {}

             
            for index, edu_form in enumerate(education_formset):
                e = edu_form.cleaned_data
                # print(index, edu_form.cleaned_data)
                
                if e.get('institution'):
                    institution = str(e.get('institution'))
                else:
                    institution = None
                
                if e.get('specialisation'):
                    specialisation = str(e.get('specialisation'))
                else:
                    specialisation = None

                if e.get('start_date'):
                    start_date = str(e.get('start_date'))
                else:
                    start_date = None
                
                if e.get('end_date'):
                    end_date = str(e.get('end_date'))
                else:
                    end_date = None
            
            
                data['Education'][f'{index}'] = {'institution': institution,
                                                'specialisation': specialisation,
                                                'start_date': start_date,
                                                'end_date': end_date,
                                            # 'description': exp_form.cleaned_data['description'],
                                        }
    
            # print(data)
            
            rdict = json.dumps(data)
            r.set(f'{CV_name}/{date_of_birth}', rdict)
            r.expire(f'{CV_name}/{date_of_birth}', 120)
            
            data_from_redis = r.get(f'{CV_name}/{date_of_birth}')
            results = json.loads(data_from_redis)

            print(results)
            return redirect(request.path_info)
    else:
        print("witam")
        personal_info_form = PersonalInfoForm()
        
        # ExperienceFormset = formset_factory(ExperienceForm, extra=9)
        experience_formset = ExperienceFormset(prefix='experience')

        # EducationFormset = formset_factory(EducationForm, extra=4)
        education_formset = EducationFormset(prefix='education')

        
    return render(request, 'tempresume/index.html', {'personal_info_form': personal_info_form, 'experience_formset': experience_formset, 'education_formset': education_formset})
