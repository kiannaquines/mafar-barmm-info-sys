from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from main.models import *

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=255, required=True)

class PersonalInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'dob' in field_name:
                field.label = 'Date of birth'
            
            if 'pob' in field_name:
                field.label = 'Place of birth'


            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = PersonalInformation
        widgets = {
            'dob': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Birth'}
            )
        }
        fields = '__all__'

class FarmProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FarmProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = FarmProfile
        fields = '__all__'
        exclude = ['related_to']

class BeneficiaryForm(forms.Form):
    personal_info = PersonalInformationForm()
    farm_profile = FarmProfileForm()

    def save(self):
        personal_info_instance = self.cleaned_data['personal_info']
        personal_info_instance.save()
        farm_profile_instance = self.cleaned_data['farm_profile']
        farm_profile_instance.related_to = personal_info_instance
        farm_profile_instance.save()
        
        return personal_info_instance, farm_profile_instance

class AdminUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AdminUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser','is_active']

class AdminUserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminUserUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']
        
        