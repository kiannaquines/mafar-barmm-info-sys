from django.urls import path
from main.views import *

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('mafar/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('mafar/users/', UsersView.as_view(), name="users"),
    path('mafar/users/add', AddUserView.as_view(), name="add_user"),
    path('mafar/users/edit/<int:pk>', UpdateUserView.as_view(), name="update_user"),
    path('mafar/users/delete/<int:pk>', DeleteUserView.as_view(), name="delete_user"),


    # Beneficiary
    path('mafar/beneficiary/', BeneficiaryView.as_view(), name="beneficiary"),
    path('mafar/beneficiary/add', AddBeneficiaryView.as_view(), name="add_beneficiary"),
]