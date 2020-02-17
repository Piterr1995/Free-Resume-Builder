from django import forms


class PersonalInfoForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    name = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField()
    address = forms.CharField(max_length=250)
    postal_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=100)

class ExperienceForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    company = forms.CharField(max_length=100, required=False)
    position = forms.CharField(max_length=100, required=False)
    description = forms.Textarea()