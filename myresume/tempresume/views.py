from django.shortcuts import render, redirect
from .forms import PersonalInfoForm, ExperienceForm, EducationForm, SkillForm, LicenseForm
from django.http import HttpResponse, HttpResponseRedirect
from redis import StrictRedis
from django.conf import settings
from django.contrib import messages
from django.forms import formset_factory
import json
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
import weasyprint
from typing import Dict, Any
# Create your views here

r = StrictRedis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def index(request):
    ExperienceFormset = formset_factory(ExperienceForm, extra=9)
    EducationFormset = formset_factory(EducationForm, extra=4)
    SkillFormset = formset_factory(SkillForm, extra=9)
    LicenseFormset = formset_factory(LicenseForm, extra=4)
    
    if request.method == "POST":
        #Personal info Form
        personal_info_form = PersonalInfoForm(request.POST)

        #Experience formset
        experience_formset = ExperienceFormset(request.POST, prefix='experience')
        
        #Education formsset
        education_formset = EducationFormset(request.POST, prefix='education')

        #Skills formset
        skill_formset = SkillFormset(request.POST, prefix="skill")

        #Licenses and Certifications formset
        license_formset = LicenseFormset(request.POST, prefix="license")


        if personal_info_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() and skill_formset.is_valid() and license_formset.is_valid():

            #Personal Info
            pi_cd = personal_info_form.cleaned_data

            CV_name = pi_cd['CV_name']
            first_name = pi_cd['first_name']
            last_name = pi_cd['last_name']
            current_position = pi_cd['current_position']
            mobile = pi_cd['mobile']
            email = pi_cd['email']
            date_of_birth = str(pi_cd['date_of_birth'])
            address = str(pi_cd['address'])
            postal_code = pi_cd['postal_code']
            city = pi_cd['city']

            data = {'Personal_info': {'first_name': first_name, 
                                    'last_name': last_name, 
                                    'current_position': current_position,
                                    'mobile': mobile,
                                    'email': email,                                    
                                    'date_of_birth': date_of_birth,
                                    'address': address,
                                    'postal_code': postal_code,
                                    'city': city}
                                    }


            # Experience
            data["Experience"] = {}

            

            for index, exp_form in enumerate(experience_formset):
                # Assigning a variable to easily get data from forms
                e = exp_form.cleaned_data

                   
                # Fields from cleaned data dictionary
                fields = ['company', 'position', 'start_date', 'end_date', 'description']
                
                #Here we will add values for each of above fields
                exp_variables = []
                
                for field in fields:
                    if e.get(field):
                        exp_variables.append(str(e.get(field)))
                    else:
                        exp_variables.append(None)
                
                # print(edu_variables)
                company = exp_variables[0]
                position = exp_variables[1]
                start_date = exp_variables[2]
                end_date = exp_variables[3]
                description = exp_variables[4]

                data['Experience'][f'{index}'] = {'company': company,
                                                'position': position,
                                                'start_date': start_date,
                                                'end_date': end_date,
                                                'description': description,
                                                }



            data['Education'] = {}

            for index, edu_form in enumerate(education_formset):
                # Assigning a variable to easily get data from forms
                e = edu_form.cleaned_data
                
                # Fields from cleaned data dictionary
                fields = ['institution', 'specialisation', 'start_date', 'end_date', 'description']
                
                #Here we will add values for each of above fields
                edu_variables = []
                
                for field in fields:
                    if e.get(field):
                        edu_variables.append(str(e.get(field)))
                    else:
                        edu_variables.append(None)
                
                # print(edu_variables)
                institution = edu_variables[0]
                specialisation = edu_variables[1]
                start_date = edu_variables[2]
                end_date = edu_variables[3]
                description = edu_variables[4]
            
                data['Education'][f'{index}'] = {'institution': institution,
                                                'specialisation': specialisation,
                                                'start_date': start_date,
                                                'end_date': end_date,
                                                'description': description,
                                        }

            #Skills and ratings
            data['Skill'] = {}
            for index, skill_form in enumerate(skill_formset):
                s = skill_form.cleaned_data

                if s.get('skill') and s.get('rating'):
                    skill = s.get('skill')
                    rating = int(s.get('rating'))
                else:
                    skill = None
                    rating = None

                data['Skill'][f'{index}'] = {
                                            'skill': skill,
                                            'rating': rating
                }


            # #Licenses and certifications
            data['License'] = {}

            for index, license_form in enumerate(license_formset):
                l = license_form.cleaned_data

                if l.get('name') and l.get('date_finished'):
                    name = l.get('name')
                    date_finished = str(l.get('date_finished'))
                else:
                    name = None
                    date_finished = None

                data['License'][f'{index}'] = {
                                            'name': name,
                                            'date_finished': date_finished,
                                            }

            

            # print(data)
            
            rdict = json.dumps(data)
            r.set(f'{CV_name}/{date_of_birth}', rdict)
            r.expire(f'{CV_name}/{date_of_birth}', 10000)
            
            print(date_of_birth)
            # data_from_redis = r.get(f'{CV_name}/{date_of_birth}')
            # results = json.loads(data_from_redis)

            # print(results)
            r_CV_name = personal_info_form.cleaned_data['CV_name']
            r_date_of_birth = personal_info_form.cleaned_data['date_of_birth']
            # slug = CV_name + "/" + date_of_birth
            
            return HttpResponseRedirect(reverse_lazy('tempresume:generate_pdf', args=[r_CV_name, r_date_of_birth]))
            # return HttpResponseRedirect(request.path_info)
    else:
        print("witam")
        personal_info_form = PersonalInfoForm()
        
        # ExperienceFormset = formset_factory(ExperienceForm, extra=9)
        experience_formset = ExperienceFormset(prefix='experience')

        # EducationFormset = formset_factory(EducationForm, extra=4)
        education_formset = EducationFormset(prefix='education')

        #SkillFormset
        skill_formset = SkillFormset(prefix="skill")

        # #Licenses and Certifications Formset
        license_formset = LicenseFormset(prefix="license")

        
    return render(request, 'tempresume/index.html', {'personal_info_form': personal_info_form, 
                                                    'experience_formset': experience_formset, 
                                                    'education_formset': education_formset, 
                                                    'skill_formset': skill_formset, 
                                                    'license_formset': license_formset,
                                                    })



def generate_pdf(request, r_CV_name, r_date_of_birth):
    data_from_redis_json = r.get(f"{r_CV_name}/{r_date_of_birth}")
    # Not generating but testing only
    # data_from_redis = r.get(f'{slug}')
    data = json.loads(data_from_redis_json)
    print(data)

    #Personal info
    pi = data['Personal_info']
    first_name = pi.get('first_name')
    last_name = pi.get('last_name')
    current_position = pi.get('current_position')
    mobile = pi.get('mobile')
    email = pi.get('email')
    date_of_birth = pi.get('date_of_birth')
    address = pi.get('address')
    postal_code = pi.get('postal_code')
    city = pi.get('city')



    def exists(_dict: Dict[str, Any], key_1: str, key_2: str = None):
        if key2:
            for index, item in enumerate(_dict.values()):
                if item.get(key_1) and item.get(key_2):
                    return True

        else:
            for index, item in enumerate(_dict.values()):
                if item[key]:
                    return True
  
    #Experience
    exp = data['Experience']

    #A variable made to check, whether pdf label should be displayed or not
    company_exists = bool(exists(exp, 'company'))
    print(company_exists)

    #Education
    edu = data['Education']

    #A variable made to check, whether pdf label should be displayed or not
    institution_exists = bool(exists(edu, 'institution'))


    #Skills
    ski = data['Skill']
    #A variable made to check, whether pdf label should be displayed or not
    skill_exists = bool(exists(ski, 'skill', 'rating'))



    #Licenses and certifications
       
    lic = data['License']
    #A variable made to check, whether pdf label should be displayed or not
    license_exists = bool(exists(lic, 'name', 'date_finished'))

    print(license_exists)

    html = render_to_string('tempresume/test.html', {'data': data, 
                                                    'first_name': first_name,
                                                    'last_name': last_name,
                                                    'current_position': current_position,
                                                    'mobile': mobile,
                                                    'email': email,
                                                    'date_of_birth': date_of_birth,
                                                    'address': address,
                                                    'postal_code': postal_code,
                                                    'city': city,
                                                    'exp': exp,
                                                    'company_exists': company_exists,
                                                    'edu': edu,
                                                    'institution_exists': institution_exists,
                                                    'ski': ski,
                                                    'skill_exists': skill_exists,
                                                    'lic': lic,
                                                    'license_exists': license_exists,
                                                

                                                    })


    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'tempresume/pdf.css')])
    return response
    # return render(request, 'tempresume/test.html', {})
