from django import forms
from datetime import datetime
from .models import EmployeeProfile


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'
        exclude = ['user','employee_photo']
        widgets = {
            'employee_dob' : forms.SelectDateWidget(years=range(1950, datetime.now().date().year))
        }
