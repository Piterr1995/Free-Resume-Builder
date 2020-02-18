from django import forms


class PersonalInfoForm(forms.Form):
    CV_name = forms.CharField(max_length=100, label="CV name")
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField()
    address = forms.CharField(max_length=250)
    postal_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=100)

class ExperienceForm(forms.Form):
    company = forms.CharField(max_length=100, required=False)
    position = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False) 
    description = forms.Textarea()

class EducationForm(forms.Form):
    institution = forms.CharField(max_length=100, required=False)
    specialisation = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    description = forms.Textarea()