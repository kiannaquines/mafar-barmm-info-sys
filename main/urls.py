from django.urls import path
from main.views import *

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('mafar/logout', logout_view, name="logout_user"),
    path('mafar/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('mafar/users/list', UsersView.as_view(), name="users"),
    path('mafar/users/add', AddUserView.as_view(), name="add_user"),
    path('mafar/users/edit/<int:pk>', UpdateUserView.as_view(), name="update_user"),
    path('mafar/users/delete/<int:pk>', DeleteUserView.as_view(), name="delete_user"),


    # Beneficiary
    path('mafar/beneficiary/list', BeneficiaryView.as_view(), name="beneficiary"),
    path('mafar/beneficiary/add', AddBeneficiaryView.as_view(), name="add_beneficiary"),
    path('mafar/beneficiary/personal/edit/<int:pk>', UpdatePersonalInfoView.as_view(), name="update_beneficiary_personal_info"),
    path('mafar/beneficiary/farm/edit/<int:pk>', UpdateFarmInfoView.as_view(), name="update_beneficiary_farm_info"),
    path('mafar/beneficiary/delete/<int:pk>', DeleteBeneficaryView.as_view(), name="remove_beneficiary_farm_info"),

    # Notification
    path('mafar/notification', NotificationView.as_view(), name="notification"),
    path('mafar/notification/add', AddNotificationView.as_view(), name="add_notification"),
    path('mafar/notification/update/<int:pk>', UpdateNotoficationInfoView.as_view(), name="update_notification"),
    path('mafar/notification/delete/<int:pk>', DeleteNotificationInfoView.as_view(), name="delete_notification"),

    # Approve and Notify
    path('mafar/approve_and_notify', ApproveAndNotifyView.as_view(), name="approve_and_notify"),

    # Report
    path('mafar/report', ReportView.as_view(), name="report"),


    path('mafar/get_barangay/list', get_barangay, name="get_barangay"),




    path('mafar/barangay', BarangayView.as_view(), name="barangay"),
    path('mafar/municipality', MunicipalityView.as_view(), name="municipality"),


]