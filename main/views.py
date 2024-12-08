from main.forms import *
from django.shortcuts import render
from django.views.generic import View, UpdateView, DeleteView, CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from main.utils import request_message
from main.mixins import MustBeLoggedIn, AlreadyLoggedInMixin

User = get_user_model()

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
    template_name = 'create_beneficiary.html'
    context = {}

    def get(self, request):
        self.context['name'] = 'Create Beneficiary'
        self.context['subtitle'] = 'Create new beneficiciary here'
        self.context['button'] = 'Create Beneficiary'
        self.context['form'] = BeneficiaryForm()
        return render(request, self.template_name, context=self.context)
    
    def post(self, request):
        pass



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

