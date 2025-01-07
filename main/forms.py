from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from main.models import *

User = get_user_model()

class ExportReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
    )
    municipality = forms.ModelChoiceField(
        empty_label="Select Municipality",
        queryset=Municpality.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Municipality",
        required=False,
    )
    barangay = forms.ModelChoiceField(
        empty_label="Select Barangay",
        queryset=Barangay.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Barangay",
        required=False,
    )

    farmer_type = forms.ChoiceField(
        required=False,
        choices=(
            ("All", "All"),
            ("Farmer", "Farmer"),
            ("Farm Worker", "Farm Worker"),
            ("Agri Youth", "Agri Youth"),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    farmer_activity = forms.ChoiceField(
        required=False,
        choices=Notification.FARMER_ACTIVITY,
        widget=forms.Select(attrs={'class': 'form-control','placeholder': 'Select activity'}),
    )

class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            
    class Meta:
        model = Notification
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=255, required=True)

class PersonalInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        
        label_mapping = {
            'dob': 'Date of birth',
            'pob': 'Place of birth',
            'name_of_household_head': 'Name of your household head',
            'is_pwd': 'Are you a person with disability?',
            'is_fourps': 'Are you a member in 4ps?',
            'is_member_in_ip': 'Are you a member in Indigenous Group?',
            'is_household_head': 'Are you a household head?',
            'is_with_government_id': 'Do you have a government ID?',
            'is_member_in_any_cooperative': 'Are you a member in any cooperative?',
            'person_to_notify': 'Person you want to notify?',
            'contact_number': 'Contact number of person you want to notify?',
            'member_in_ip_specific': 'Specify what Indigenous Group are you',
            'relationship': 'Relationship to household head'
        }

        choices_mapping_props = {
            'gender': {
                'choices': PersonalInformation.GENDER,
                'required': True,
            },
            'education': {
                'choices': PersonalInformation.HIGHEST_EDUCATION,
                'required': True,
            },
            'religion': {
                'choices': PersonalInformation.RELIGION,
                'required': True,
            },
            'civil_status': {
                'choices': PersonalInformation.CIVIL_STATUS,
                'required': True,
            },
            'extension': {
                'choices': PersonalInformation.EXTENSIONS,
                'required': False,
            },
            'relationship': {
                'choices': PersonalInformation.RELATIONSHIP,
                'required': True,
            },
        }

        for field in choices_mapping_props:
            self.fields[field].choices = choices_mapping_props[field]['choices']
            self.fields[field].required = choices_mapping_props[field]['required']

        for field_name, field in self.fields.items():
            if field_name in label_mapping:
                field.label = label_mapping[field_name]
            
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = PersonalInformation
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Birth'}
            )
        }

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
        

class BarangayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BarangayForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = Barangay
        fields = '__all__'


class MunicipalityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MunicipalityForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = Municpality
        fields = '__all__'
