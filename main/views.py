from io import BytesIO
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    CreateView,
    FormView,
    ListView,
)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from main.mixins import MustBeLoggedIn, AlreadyLoggedInMixin
from core.settings import BARRM_LOGO_PATH, MFAR_LOGO_PATH, SERVER_SMS_MESSAGE_TEMPLATE
from main.utils import request_message
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from main.service import *
from main.forms import *
from django.utils import timezone
from datetime import datetime, time
from django.shortcuts import redirect, render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import json
from django.db.models import Q, Count
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from django.conf import settings
import os


User = get_user_model()


def get_barangay(request):
    if request.method == "POST":
        data = json.loads(request.body)
        municipality_id = data.get("municipality_id")

        if municipality_id == "":
            barangay_list = [
                {"id": barangay.pk, "name": barangay.barangay}
                for barangay in Barangay.objects.all()
            ]
        else:
            barangay_list = [
                {"id": barangay.pk, "name": barangay.barangay}
                for barangay in Barangay.objects.filter(
                    municipality=municipality_id
                ).all()
            ]

        return JsonResponse({"barangay": barangay_list})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def logout_view(request):
    logout(request)
    request_message(
        request=request,
        message="You have successfully logged out. Thank you!",
        tag="primary",
    )
    return redirect("login")


class NotificationView(MustBeLoggedIn, View):
    template_name = "notification.html"
    context = {}

    def get(self, request):
        self.context["items"] = Notification.objects.order_by("-date_added")
        return render(request, self.template_name, self.context)

    def post(self, request):
        notification = Notification.objects.filter(id=request.POST.get("id")).first()
        beneficiaries_within_place = FarmProfile.objects.filter(
            Q(activity_farmer__iexact=request.POST.get("activity"))
            | Q(activity_farmworker__iexact=request.POST.get("activity")),
            related_to__municipality=notification.for_municipality,
            main_livelihood=request.POST.get("type"),
        )

        message = notification.message
        mobile = [
            beneficiary.related_to.mobile_number
            for beneficiary in beneficiaries_within_place
        ]

        sms_notification = send_sms_api_interface(message, mobile)
        return JsonResponse(sms_notification)


class AddNotificationView(CreateView):
    template_name = "includes/form.html"
    form_class = NotificationForm
    model = Notification
    success_url = reverse_lazy("notification")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Create Notification"
        context["subtitle"] = "Create new notification here"
        context["button"] = "Create Notification"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully created a new notification",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class UpdateNotoficationInfoView(UpdateView):
    pk_url_kwarg = "pk"
    model = Notification
    form_class = NotificationForm
    template_name = "includes/form.html"
    success_url = reverse_lazy("notification")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Notification Information"
        context["subtitle"] = "Update Notification Information"
        context["button"] = "Update Information"

        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully updated notification information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")
        return super().form_invalid(form)


class DeleteNotificationInfoView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = "pk"
    model = Notification
    template_name = "includes/delete.html"
    success_url = reverse_lazy("notification")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Delete Notification"
        context["subtitle"] = "Delete notification details here"
        context["button"] = "Delete Notification"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully deleted notification information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class ApproveAndNotifyView(View):
    def post(self, request):
        beneficiary_id = request.POST.get("id")

        beneficiary = get_object_or_404(FarmProfile, id=beneficiary_id)
        beneficiary.status = "Approved"
        beneficiary.save()

        message = SERVER_SMS_MESSAGE_TEMPLATE.format(
            client_fullname=beneficiary.related_to.get_full_name()
        )
        mobile = [beneficiary.related_to.mobile_number]

        sms_notification = send_sms_api_interface(message, mobile)
        return JsonResponse(sms_notification)


class LoginView(AlreadyLoggedInMixin, FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            request_message(
                request=self.request,
                message="You have successfully logged in. Thank you!",
                tag="primary",
            )
            return super().form_valid(form)
        else:
            request_message(
                request=self.request,
                message="Invalid username or password",
                tag="danger",
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")

        return super().form_invalid(form)


class DashboardView(MustBeLoggedIn, View):
    template_name = "dashboard.html"
    context = {}

    def get(self, request):
        self.context["pending_count"] = FarmProfile.objects.filter(
            status="Pending"
        ).count()
        self.context["approved_count"] = FarmProfile.objects.filter(
            status="Approved"
        ).count()
        self.context["disapproved_count"] = FarmProfile.objects.filter(
            status="Disapproved"
        ).count()
        self.context["total_beneficiaries"] = FarmProfile.objects.count()
        self.context["items"] = FarmProfile.objects.all().order_by("-date_added")[:10]
        return render(request, self.template_name, self.context)


def add_logo(canvas, doc):
    logo_width = 0.7 * inch
    logo_height = 0.7 * inch

    left_x = doc.leftMargin
    left_y = doc.pagesize[1] - 1.3 * inch
    canvas.drawImage(
        BARRM_LOGO_PATH,
        x=left_x,
        y=left_y,
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
        mask="auto",
    )

    right_x = doc.pagesize[0] - doc.rightMargin - logo_width
    right_y = doc.pagesize[1] - 1.3 * inch
    canvas.drawImage(
        MFAR_LOGO_PATH,
        x=right_x,
        y=right_y,
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
        mask="auto",
    )


class OverallReport(View):
    template_name = "overall_report.html"

    def get(self, request):
        context = {}
        context["items"] = FarmProfile.objects.all().order_by("-date_added")[:10]
        context["filter_form"] = FilterOverAllBeneficiary()
        return render(request, self.template_name, context)

    def post(self, request):
        form = FilterOverAllBeneficiary(request.POST)

        if form.is_valid():
            municipality = form.cleaned_data["municipality"]
            activity = form.cleaned_data["activity"]
            livelihood = form.cleaned_data["livelihood"]

            query = FarmProfile.objects.all().filter(status="Approved")

            if municipality:
                query = query.filter(related_to__municipality=municipality)

            if activity:
                query = query.filter(
                    Q(activity_farmer__iexact=activity)
                    | Q(activity_farmworker__iexact=activity)
                )

            if livelihood:
                query = query.filter(main_livelihood__iexact=livelihood)

            grouped_data = (
                query.values(
                    "related_to__municipality__municipality",
                    "main_livelihood",
                    "activity_farmer",
                    "activity_farmworker",
                )
                .annotate(total=Count("id"))
                .order_by("related_to__municipality__municipality")
            )

            if grouped_data.count() == 0:
                request_message(
                    request=request,
                    message="No data found matching the provided filters",
                    tag="danger",
                )
                return redirect(reverse_lazy("overall_report"))

            total_count = 0

            data = [
                [
                    "Municipality",
                    "Main Livelihood",
                    "Farmer Activity",
                    "Beneficiaries",
                    "Total",
                ]
            ]

            for item in grouped_data:
                municipality_name = item["related_to__municipality__municipality"]
                main_livelihood = item["main_livelihood"]
                activity = item["activity_farmer"] or item["activity_farmworker"]
                beneficiaries = item["total"]
                total_count += beneficiaries
                data.append(
                    [
                        municipality_name,
                        main_livelihood,
                        activity,
                        beneficiaries,
                        "",
                    ]
                )

            data.append(
                [
                    "",
                    "",
                    "",
                    "Total Beneficiaries",
                    str(total_count),
                ]
            )

            buffer = BytesIO()
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="overall_report.pdf"'

            left_margin = 0.5 * inch
            right_margin = 0.5 * inch
            top_margin = 0.5 * inch
            bottom_margin = 1 * inch
            elements = []
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                leftMargin=left_margin,
                rightMargin=right_margin,
                topMargin=top_margin,
                bottomMargin=bottom_margin,
            )
            doc.build(elements, onFirstPage=add_logo)
            doc.title = "Beneficiaries Overall Report"

            styles = getSampleStyleSheet()
            header_style = styles["Heading2"]
            header_style.alignment = 1

            current_date = datetime.now().strftime("%Y-%m-%d")
            header = Paragraph(
                f"MAFAR BARRM SGA<br/>Overall Beneficiary Report<br/><small>As of {current_date}</small>",
                header_style,
            )
            elements.append(header)
            elements.append(Spacer(1, 0.2 * inch))

            green_color = colors.Color(61 / 255, 117 / 255, 85 / 255)

            available_width = doc.width
            num_columns = len(data[0])
            column_width = available_width / num_columns

            table = Table(data, colWidths=[column_width] * num_columns)
            style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), green_color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
            table.setStyle(style)
            elements.append(table)
            elements.append(Spacer(1, 0.5 * inch))
            prepared_by_style = ParagraphStyle(
                name="PreparedByStyle",
                fontName="Helvetica-Bold",
                fontSize=10,
                textTransform="uppercase",
                spaceBefore=0,
                spaceAfter=0,
                leftIndent=0,
                rightIndent=0,
            )
            elements.append(
                Paragraph(f"Prepared by: {request.user}", style=prepared_by_style)
            )
            doc.build(elements)

            buffer.seek(0)
            response.write(buffer.read())
            return response

        request_message(
            request=request,
            message="Invalid form data. Please check your inputs and try again.",
            tag="danger",
        )
        return redirect("overall_report")


class ReportView(MustBeLoggedIn, View):
    template_name = "report.html"
    context = {}

    def get(self, request):
        self.context["items"] = FarmProfile.objects.all().order_by("-date_added")[:10]
        self.context["export_form"] = ExportReportForm()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ExportReportForm(request.POST)

        if form.is_valid():
            start_date = timezone.make_aware(
                datetime.combine(form.cleaned_data["start_date"], time.min)
            )
            end_date = timezone.make_aware(
                datetime.combine(form.cleaned_data["end_date"], time.max)
            )
            municipality = form.cleaned_data["municipality"]
            barangay = form.cleaned_data["barangay"]
            farmer_type = form.cleaned_data["farmer_type"]
            farmer_activity = form.cleaned_data["farmer_activity"]

            if farmer_type == "All":
                query = FarmProfile.objects.filter(
                    date_added__range=(start_date, end_date),
                ).order_by("-date_added").filter(status="Approved")
            else:
                query = FarmProfile.objects.filter(
                    date_added__range=(start_date, end_date),
                    main_livelihood=farmer_type,
                ).order_by("-date_added").filter(status="Approved")

            if municipality:
                header_first = municipality
                query = query.filter(related_to__municipality=municipality)
            else:
                header_first = "All Municipality"

            if barangay:
                header_secondary = barangay
                query = query.filter(related_to__barangay=barangay)
            else:
                header_secondary = "All Barangay"

            if farmer_activity:
                header_secondary = farmer_activity
                query = query.filter(
                    Q(activity_farmer__iexact=farmer_activity)
                    | Q(activity_farmworker__iexact=farmer_activity)
                )
            else:
                header_secondary = "All Farmer Activities"

            if not query.exists():
                request_message(
                    request=request,
                    message="Sorry, no data found with your filter provided, please try again.",
                    tag="danger",
                )
                return redirect("report")

            buffer = BytesIO()
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                'inline; filename="beneficiary_report.pdf"'
            )

            left_margin = 0.5 * inch
            right_margin = 0.5 * inch
            top_margin = 0.5 * inch
            bottom_margin = 1 * inch
            elements = []

            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                leftMargin=left_margin,
                rightMargin=right_margin,
                topMargin=top_margin,
                bottomMargin=bottom_margin,
            )

            doc.build(elements, onFirstPage=add_logo)
            doc.title = "Beneficiaries Report"

            styles = getSampleStyleSheet()
            header_style = styles["Heading2"]
            header_style.alignment = 1

            current_date = datetime.now().strftime("%Y-%m-%d")
            header = Paragraph(
                f"MAFAR BARRM SGA<br/>{header_first}<br/>{header_secondary}<br/><small>As of {current_date}</small>",
                header_style,
            )
            elements.append(header)
            elements.append(Spacer(1, 0.4 * inch))
            data = [
                [
                    "Beneficiary",
                    "Mobile Number",
                    "Gender",
                    "Status",
                    "Municipality",
                    "Barangay",
                    "Main Livelihood",
                ]
            ]
            for item in query:
                data.append(
                    [
                        str(item.related_to.get_full_name()),
                        item.related_to.gender,
                        item.related_to.mobile_number,
                        item.status,
                        item.related_to.municipality,
                        item.related_to.barangay,
                        item.main_livelihood,
                    ]
                )

            green_color = colors.Color(61 / 255, 117 / 255, 85 / 255)

            table = Table(data)
            style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), green_color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
            table.setStyle(style)
            elements.append(table)
            elements.append(Spacer(1, 0.5 * inch))

            prepared_by_style = ParagraphStyle(
                name="PreparedByStyle",
                fontName="Helvetica-Bold",
                fontSize=10,
                textTransform="uppercase",
                spaceBefore=0,
                spaceAfter=0,
                leftIndent=0,
                rightIndent=0,
            )
            elements.append(
                Paragraph(f"Prepared by: {request.user}", style=prepared_by_style)
            )

            doc.build(elements)

            buffer.seek(0)
            response.write(buffer.read())
            return response


class BeneficiaryView(MustBeLoggedIn, View):
    template_name = "beneficiary.html"

    def get(self, request):
        context = {}
        main_query = FarmProfile.objects.all()

        filter_form = FilterBeneficiary(request.GET)
        context["filter_form"] = filter_form

        if filter_form.is_valid():
            filters = request.GET

            query = Q()

            if filters.get("farmer_activity"):
                query &= Q(activity_farmer__iexact=filters.get("farmer_activity")) | Q(
                    activity_farmworker__iexact=filters.get("farmer_activity")
                )

            if filters.get("municipality"):
                query &= Q(related_to__municipality=filters.get("municipality"))

            if filters.get("barangay"):
                query &= Q(related_to__barangay=filters.get("barangay"))

            main_query = main_query.filter(query)

        context["beneficiaries"] = main_query
        return render(request, self.template_name, context)


class AddBeneficiaryView(View):
    template_name = "form_beneficiary.html"

    def get_context_data(self, form=None):
        return {
            "name": "Create Beneficiary",
            "subtitle": "Create new beneficiary here",
            "button": "Create Beneficiary",
            "form": form or BeneficiaryForm(),
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

            request_message(
                request=request,
                message="You have successfully created a new beneficiary",
                tag="primary",
            )
            return redirect("beneficiary")

        else:

            for field, errors in personal_info_form.errors.items():
                for error in errors:
                    request_message(
                        request=request, message=f"{field} {error}", tag="danger"
                    )

            for field, errors in farm_profile_form.errors.items():
                for error in errors:
                    request_message(
                        request=request, message=f"{field} {error}", tag="danger"
                    )

            return render(
                request,
                self.template_name,
                {
                    "name": "Create Beneficiary",
                    "subtitle": "Create new beneficiary here",
                    "button": "Create Beneficiary",
                    "form": BeneficiaryForm(),
                },
            )


class UpdatePersonalInfoView(UpdateView):
    pk_url_kwarg = "pk"
    model = PersonalInformation
    form_class = PersonalInformationForm
    template_name = "includes/form.html"
    success_url = reverse_lazy("beneficiary")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Information"
        context["subtitle"] = "Update Personal Information"
        context["button"] = "Update Information"

        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully updated personal information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")
        return super().form_invalid(form)


class UpdateFarmInfoView(UpdateView):
    pk_url_kwarg = "pk"
    model = FarmProfile
    form_class = FarmProfileForm
    template_name = "includes/form.html"
    success_url = reverse_lazy("beneficiary")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Farm Information"
        context["subtitle"] = "Update Farm Information"
        context["button"] = "Update Information"

        return context

    def form_valid(self, form):

        if form.instance.status in ["Disapproved", "Approved"]:
            form = super().form_valid(form)
            get_farmer_info = FarmProfile.objects.filter(
                id=self.kwargs.get("pk", None)
            ).first()
            message = SERVER_SMS_MESSAGE_TEMPLATE.format(
                client_fullname=get_farmer_info.related_to.get_full_name(),
                status=get_farmer_info.status,
            )
            mobile = [get_farmer_info.related_to.mobile_number]
            send_sms_api_interface(message, mobile)
            request_message(
                request=self.request,
                message=f"You have successfully updated and notify beneficiary with {get_farmer_info.status} status",
                tag="primary",
            )
            return form

        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")
        return super().form_invalid(form)


class UsersView(MustBeLoggedIn, ListView):
    template_name = "users.html"
    model = User
    context_object_name = "users"
    queryset = User.objects.all()


class AddUserView(CreateView):
    template_name = "includes/form.html"
    form_class = AdminUserForm
    model = User
    success_url = reverse_lazy("users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Create User"
        context["subtitle"] = "Create new user here"
        context["button"] = "Create User"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully created a new user",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class UpdateUserView(MustBeLoggedIn, UpdateView):
    pk_url_kwarg = "pk"
    template_name = "includes/form.html"
    form_class = AdminUserUpdateForm
    model = User
    success_url = reverse_lazy("users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Update User"
        context["subtitle"] = "Update user details here"
        context["button"] = "Update User"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have updated user information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class DeleteUserView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = "pk"
    model = User
    template_name = "includes/delete.html"
    success_url = reverse_lazy("users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Delete User"
        context["subtitle"] = "Delete user details here"
        context["button"] = "Delete User"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully deleted user information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class DeleteBeneficaryView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = "pk"
    model = PersonalInformation
    template_name = "includes/delete.html"
    success_url = reverse_lazy("beneficiary")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Delete Beneficiary"
        context["subtitle"] = "Delete beneficiary details here"
        context["button"] = "Delete Beneficiary"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully deleted beneficiary information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class MunicipalityView(MustBeLoggedIn, View):
    template_name = "municipality.html"
    context = {}

    def get(self, request):
        self.context["items"] = Municpality.objects.order_by("-date_added")
        return render(request, self.template_name, self.context)


class BarangayView(MustBeLoggedIn, View):
    template_name = "barangay.html"
    context = {}

    def get(self, request):
        self.context["items"] = Barangay.objects.order_by("-date_added")
        return render(request, self.template_name, self.context)


class AddMunicipalityView(CreateView):
    template_name = "includes/form.html"
    form_class = MunicipalityForm
    model = Municpality
    success_url = reverse_lazy("municipality")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Create Municipality"
        context["subtitle"] = "Create new municipality here"
        context["button"] = "Create Municipality"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully created a new municipality",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class AddBarangayView(CreateView):
    template_name = "includes/form.html"
    form_class = BarangayForm
    model = Barangay
    success_url = reverse_lazy("barangay")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Create Barangay"
        context["subtitle"] = "Create new barangay here"
        context["button"] = "Create Barangay"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully created a new barangay",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class UpdateBarangayView(UpdateView):
    template_name = "includes/form.html"
    form_class = BarangayForm
    model = Barangay
    success_url = reverse_lazy("barangay")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Barangay"
        context["subtitle"] = "Update new barangay here"
        context["button"] = "Update Barangay"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully update a new barangay",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class UpdateMunicipalityView(UpdateView):
    template_name = "includes/form.html"
    form_class = MunicipalityForm
    model = Municpality
    success_url = reverse_lazy("municipality")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Municpality"
        context["subtitle"] = "Update new municpality here"
        context["button"] = "Update Municpality"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully update a new municipality",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class DeleteBarangayView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = "pk"
    model = Barangay
    template_name = "includes/delete.html"
    success_url = reverse_lazy("barangay")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Delete Barangay"
        context["subtitle"] = "Delete barangay details here"
        context["button"] = "Delete Barangay"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully deleted barangay information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")


class DeleteMunicipalityView(MustBeLoggedIn, DeleteView):
    pk_url_kwarg = "pk"
    model = Municpality
    template_name = "includes/delete.html"
    success_url = reverse_lazy("municipality")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Delete Municipality"
        context["subtitle"] = "Delete municipality details here"
        context["button"] = "Delete Municipality"
        return context

    def form_valid(self, form):
        request_message(
            request=self.request,
            message="You have successfully deleted municipality information",
            tag="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                request_message(request=self.request, message=error, tag="danger")
