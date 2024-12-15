from django.http import JsonResponse
from main.forms import *
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, UpdateView, DeleteView, CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from main.utils import request_message
from main.mixins import MustBeLoggedIn, AlreadyLoggedInMixin
from main.service import *
from core.settings import SERVER_SMS_MESSAGE_TEMPLATE
User = get_user_model()

def logout_view(request):
    logout(request)
    request_message(request=request, message="You have successfully logged out. Thank you!", tag="primary")
    return redirect('login')

class NotificationView(MustBeLoggedIn, View):
    template_name = 'notification.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)


class ApproveAndNotifyView(View):
    def post(self, request):
        beneficiary_id = request.POST.get('id')

        beneficiary = get_object_or_404(FarmProfile, id=beneficiary_id)
        beneficiary.status = "Approved"
        beneficiary.save()

        message = SERVER_SMS_MESSAGE_TEMPLATE.format(client_fullname=beneficiary.related_to.get_full_name())
        mobile = beneficiary.related_to.mobile_number

        sms_notification = send_sms_api_interface(message, mobile)
        return JsonResponse(sms_notification)


class LoginView(AlreadyLoggedInMixin, FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            request_message(request=self.request, message="You have successfully logged in. Thank you!", tag="primary")
            return super().form_valid(form)
        else:
            request_message(request=self.request, message="Invalid username or password", tag="danger")
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")

        return super().form_invalid(form)
    
class DashboardView(MustBeLoggedIn, View):
    template_name = 'dashboard.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

class BeneficiaryView(MustBeLoggedIn, ListView):
    template_name = 'beneficiary.html'
    model = FarmProfile
    context_object_name = 'beneficiaries'
    queryset = FarmProfile.objects.all()

class AddBeneficiaryView(View):
    template_name = 'form_beneficiary.html'

    def get_context_data(self, form=None):
        return {
            'name': 'Create Beneficiary',
            'subtitle': 'Create new beneficiary here',
            'button': 'Create Beneficiary',
            'form': form or BeneficiaryForm(),
        }

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        personal_info_form = PersonalInformationForm(request.POST)
        farm_profile_form = FarmProfileForm(request.POST)

        if personal_info_form.is_valid() and farm_profile_form.is_valid():
            personal_info = personal_info_form.save()

            farm_profile = farm_profile_form.save(commit=False)
            farm_profile.related_to = personal_info
            farm_profile.save()

            request_message(request=request, message='You have successfully created a new beneficiary', tag='primary')
            return redirect('beneficiary')
        
        else:

            for field, errors in personal_info_form.errors.items():
                for error in errors:
                    request_message(request=request, message=f'{field} {error}', tag="danger")

            for field, errors in farm_profile_form.errors.items():
                for error in errors:
                    request_message(request=request, message=f'{field} {error}', tag="danger")
            
            return render(request, self.template_name, {
                'name': 'Create Beneficiary',
                'subtitle': 'Create new beneficiary here',
                'button': 'Create Beneficiary',
                'form': BeneficiaryForm(),
            })

class UpdatePersonalInfoView(UpdateView):
    pk_url_kwarg = 'pk'
    model = PersonalInformation
    form_class = PersonalInformationForm
    template_name = 'includes/form.html'
    success_url = reverse_lazy('beneficiary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Update Information'
        context['subtitle'] = 'Update Personal Information'
        context['button'] = 'Update Information'

        return context
    def form_valid(self, form):
        request_message(request=self.request, message='You have successfully updated personal information', tag='primary')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")
        return super().form_invalid(form)
    
class UpdateFarmInfoView(UpdateView):
    pk_url_kwarg = 'pk'
    model = FarmProfile
    form_class = FarmProfileForm
    template_name = 'includes/form.html'
    success_url = reverse_lazy('beneficiary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Update Farm Information'
        context['subtitle'] = 'Update Farm Information'
        context['button'] = 'Update Information'

        return context
    def form_valid(self, form):
        request_message(request=self.request, message='You have successfully updated farm information', tag='primary')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")
        return super().form_invalid(form)

class UsersView(MustBeLoggedIn, ListView):
    template_name = 'users.html'
    model = User
    context_object_name = 'users'
    queryset = User.objects.all()

class AddUserView(CreateView):
    template_name = 'includes/form.html'
    form_class = AdminUserForm
    model = User
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Create User'
        context['subtitle'] = 'Create new user here'
        context['button'] = 'Create User'
        return context

    def form_valid(self, form):
        request_message(request=self.request, message='You have successfully created a new user', tag='primary')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")

class UpdateUserView(MustBeLoggedIn, UpdateView):
    pk_url_kwarg = 'pk'
    template_name = 'includes/form.html'
    form_class = AdminUserUpdateForm
    model = User
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Update User'
        context['subtitle'] = 'Update user details here'
        context['button'] = 'Update User'
        return context
    
    def form_valid(self, form):
        request_message(request=self.request, message='You have updated user information', tag='primary')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")

class DeleteUserView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = 'pk'
    model = User
    template_name = 'includes/delete.html'
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delete User'
        context['subtitle'] = 'Delete user details here'
        context['button'] = 'Delete User'
        return context
    
    def form_valid(self, form):
        request_message(request=self.request, message='You have successfully deleted user information', tag='primary')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")

class DeleteBeneficaryView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = 'pk'
    model = PersonalInformation
    template_name = 'includes/delete.html'
    success_url = reverse_lazy('beneficiary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delete Beneficiary'
        context['subtitle'] = 'Delete beneficiary details here'
        context['button'] = 'Delete Beneficiary'
        return context
    
    def form_valid(self, form):
        request_message(request=self.request, message='You have successfully deleted beneficiary information', tag='primary')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")