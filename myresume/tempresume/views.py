from django.shortcuts import render, redirect
from .forms import PersonalInfoForm, ExperienceForm, EducationForm
from django.http import HttpResponse, HttpResponseRedirect
from redis import StrictRedis
from django.conf import settings
from django.contrib import messages
from django.forms import formset_factory
import json

# Create your views here

r = StrictRedis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# def index(request):
#     if request.method == "POST":
#         #Personal info Form
#         personal_info_form = PersonalInfoForm(request.POST)

#         #Experience forms
#         exp_1_form = exp_2_form = exp_3_form = exp_4_form = exp_5_form = exp_6_form = exp_7_form = exp_8_form = exp_9_form = exp_10_form = ExperienceForm(request.POST)
#         exp_forms = [exp_1_form, exp_2_form, exp_3_form, exp_4_form, exp_5_form, exp_6_form, exp_7_form, exp_8_form, exp_9_form, exp_10_form]
        
#         #Education forms
#         edu_1_form = edu_2_form = edu_3_form = edu_4_form = edu_5_form = EducationForm(request.POST)
#         edu_forms = [edu_1_form, edu_2_form, edu_3_form, edu_4_form, edu_5_form]

#         if personal_info_form.is_valid() and [exp_form.is_valid() for exp_form in exp_forms] and [edu_form.is_valid() for edu_form in edu_forms]:

#             #Personal Info
#             CV_name = personal_info_form.cleaned_data['CV_name']
#             first_name = personal_info_form.cleaned_data['first_name']
#             last_name = personal_info_form.cleaned_data['last_name']
#             date_of_birth = str(personal_info_form.cleaned_data['date_of_birth'])
#             address = str(personal_info_form.cleaned_data['address'])
#             postal_code = personal_info_form.cleaned_data['postal_code']
#             city = personal_info_form.cleaned_data['city']

#             data = {'Personal_info': {'first_name': first_name, 
#                                     'last_name': last_name, 
#                                     'date_of_birth': date_of_birth,
#                                     'address': address,
#                                     'postal_code': postal_code,
#                                     'city': city}
#             }


#             #Experience
#             data["Experience"] = {}

#             for index, exp_form in enumerate(exp_forms):
#                 # if exp_form.cleaned_data['start_date'] == '':
#                 #     start_date = None
#                 # else:
#                 #     start_date = exp_form.cleaned_data['start_date']
                
#                 # if exp_form.cleaned_data['end_date'] == '':
#                 #     end_date = None
#                 # else:
#                 #     end_date = str(exp_form.cleaned_data['end_date'])
                
#                 # if exp_form.cleaned_data['company'] == '':
#                 #     company = None
#                 # else:
#                 #     company = str(exp_form.cleaned_data['company'])

#                 # if exp_form.cleaned_data['position'] == '':
#                 #     position = None
#                 # else:
#                 #     position = str(exp_form.cleaned_data['position'])

#                 data['Experience'][f'{index}'] = {'company': exp_form.cleaned_data['company'],
#                                                 'position': exp_form.cleaned_data['position'],
#                                                 'start_date': exp_form.cleaned_data['start_date'],
#                                                 'end_date': exp_form.cleaned_data['end_date'],
#                                             # 'description': exp_form.cleaned_data['description'],
#                                             }


#             data['Education'] = {}

#             for index, edu_form in enumerate(edu_forms):
#                 start_date = str(edu_form.cleaned_data['start_date'])
#                 end_date = str(edu_form.cleaned_data['end_date'])
                
#                 if edu_form.cleaned_data['institution']:
#                     institution = str(edu_form.cleaned_data['institution'])
#                 else:
#                     institution = None
                
#                 if edu_form.cleaned_data['specialisation']:
#                     specialisation = str(edu_form.cleaned_data['specialistation'])
#                 else:
#                     specialisation = None
                
                
#                 data['Education'][f'{index}'] = {'institution': institution,
#                                                 'specialisation': specialisation,
#                                                 'start_date': start_date,
#                                                 'end_date': end_date,
#                                             # 'description': exp_form.cleaned_data['description'],
#                                             }
      
#             print(data)
            
#             rdict = json.dumps(data)
#             r.set(f'{CV_name}/{date_of_birth}', rdict)
#             r.expire(f'{CV_name}/{date_of_birth}', 120)
            
#             data_from_redis = r.get(f'{CV_name}/{date_of_birth}')
#             results = json.loads(data_from_redis)

#             print(results)
#             return redirect('www.fcbarca.com')
#     else:
#         print("witam")
#         personal_info_form = PersonalInfoForm()
        
#         exp1_form = exp2_form = exp3_form = exp4_form = exp5_form = exp6_form = exp7_form = exp8_form = exp9_form = exp10_form = ExperienceForm()
#         exp_forms = [exp1_form, exp2_form, exp3_form, exp4_form, exp5_form, exp6_form, exp7_form, exp8_form, exp9_form, exp10_form]

#         edu_1_form = edu_2_form = edu_3_form = edu_4_form = edu_5_form = EducationForm()
#         edu_forms = [edu_1_form, edu_2_form, edu_3_form, edu_4_form, edu_5_form]

        
#     return render(request, 'tempresume/index.html', {'personal_info_form': personal_info_form, 'exp_forms': exp_forms, 'edu_forms': edu_forms})

 

def index(request):
    if request.method == "POST":
        #Personal info Form
        personal_info_form = PersonalInfoForm(request.POST)

        #Experience forms
        # exp_1_form = exp_2_form = exp_3_form = exp_4_form = exp_5_form = exp_6_form = exp_7_form = exp_8_form = exp_9_form = exp_10_form = ExperienceForm(request.POST)
        # exp_forms = [exp_1_form, exp_2_form, exp_3_form, exp_4_form, exp_5_form, exp_6_form, exp_7_form, exp_8_form, exp_9_form, exp_10_form]

        ExperienceFormset = formset_factory(ExperienceForm, extra=9)
        experience_formset = ExperienceFormset(request.POST, prefix='experience')
        
        #Education forms
        # edu_1_form = edu_2_form = edu_3_form = edu_4_form = edu_5_form = EducationForm(request.POST)
        # edu_forms = [edu_1_form, edu_2_form, edu_3_form, edu_4_form, edu_5_form]
        EducationFormset = formset_factory(EducationForm, extra=4)
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

            data = {'Personal_info': {'first_name': first_name, 
                                    'last_name': last_name, 
                                    'date_of_birth': date_of_birth,
                                    'address': address,
                                    'postal_code': postal_code,
                                    'city': city}
            }


            #Experience
            data["Experience"] = {}

            for index, exp_form in enumerate(experience_formset):
                print(index, exp_form.cleaned_data)
                # data['Experience'][f'{index}'] = {'company': exp_form.cleaned_data['company'],
                #                                 'position': exp_form.cleaned_data['position'],
                #                                 'start_date': exp_form.cleaned_data['start_date'],
                #                                 'end_date': exp_form.cleaned_data['end_date'],
                #                             # 'description': exp_form.cleaned_data['description'],
                #                             }


            data['Education'] = {}

            for index, edu_form in enumerate(education_formset):
                print(index, edu_form.cleaned_data)

                # start_date = str(edu_form.cleaned_data['start_date'])
                # end_date = str(edu_form.cleaned_data['end_date'])
                
                # if edu_form.cleaned_data['institution']:
                #     institution = str(edu_form.cleaned_data['institution'])
                # else:
                #     institution = None
                
                # if edu_form.cleaned_data['specialisation']:
                #     specialisation = str(edu_form.cleaned_data['specialistation'])
                # else:
                #     specialisation = None
                
                
                # data['Education'][f'{index}'] = {'institution': institution,
                #                                 'specialisation': specialisation,
                #                                 'start_date': start_date,
                #                                 'end_date': end_date,
                #                             # 'description': exp_form.cleaned_data['description'],
                #                             }
        
            # print(data)
            
            # rdict = json.dumps(data)
            # r.set(f'{CV_name}/{date_of_birth}', rdict)
            # r.expire(f'{CV_name}/{date_of_birth}', 120)
            
            # data_from_redis = r.get(f'{CV_name}/{date_of_birth}')
            # results = json.loads(data_from_redis)

            # print(results)
            # return redirect('www.fcbarca.com')
    else:
        print("witam")
        personal_info_form = PersonalInfoForm()
        
        ExperienceFormset = formset_factory(ExperienceForm, extra=9)
        experience_formset = ExperienceFormset(prefix='experience')

        EducationFormset = formset_factory(EducationForm, extra=4)
        education_formset = EducationFormset(prefix='education')

        
    return render(request, 'tempresume/index.html', {'personal_info_form': personal_info_form, 'experience_formset': experience_formset, 'education_formset': education_formset})


def experience(request):
    