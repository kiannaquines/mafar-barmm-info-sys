from django.db import models


class Barangay(models.Model):
    barangay = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Barangay"
        verbose_name = "Barangay"

    def __str__(self) -> str:
        return self.barangay


class Municpality(models.Model):
    municipality = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Municipality"
        verbose_name = "Municipality"

    def __str__(self) -> str:
        return self.municipality


class PersonalInformation(models.Model):
    EXTENSIONS = (
        ("None", "None"),
        ("Sr.", "Sr."),
        ("Jr.", "Jr."),
    )

    GENDER = (("Male", "Male"), ("Female", "Female"))

    HIGHEST_EDUCATION = (
        ("Pre-school", "Pre-school"),
        ("Elementary", "Elementary"),
        ("High School", "High School"),
        ("Junior High School", "Junior High School"),
        ("Senior High School", "Senior High School"),
        ("College", "College"),
        ("Vocational", "Vocational"),
        ("Post-graduate", "Post-graduate"),
        ("None", "None"),
    )

    RELIGION = (
        ("Christianity", "Christianity"),
        ("Islam", "Islam"),
        ("Others", "Others"),
    )

    CIVIL_STATUS = (
        ("Single", "Single"),
        ("Married", "Married"),
        ("Widowed", "Widowed"),
        ("Separated", "Separated"),
    )

    RELATIONSHIP = (
        ("Mother", "Mother"),
        ("Father", "Father"),
    )

    firstname = models.CharField(
        max_length=255, help_text="Beneficiary first name", db_index=True
    )
    middlename = models.CharField(
        max_length=255, help_text="Beneficiary middle name", db_index=True
    )
    lastname = models.CharField(
        max_length=255, help_text="Beneficiary last name", db_index=True
    )
    extension = models.CharField(
        max_length=255,
        help_text="Extension",
        choices=EXTENSIONS,
        db_index=True,
        null=True,
        blank=True,
    )
    gender = models.CharField(max_length=255, help_text="Gender", choices=GENDER)

    purok = models.CharField(max_length=255, help_text="Purok")
    municipality = models.ForeignKey(
        Municpality, on_delete=models.CASCADE, help_text="Municipality"
    )
    barangay = models.ForeignKey(
        Barangay, on_delete=models.CASCADE, help_text="Barangay"
    )
    street = models.CharField(max_length=255, help_text="Street")
    province = models.CharField(max_length=255, help_text="Province")
    region = models.CharField(max_length=255, help_text="Region")

    mobile_number = models.CharField(max_length=11, help_text="Mobile Number")
    landline_number = models.CharField(
        max_length=255, help_text="Landline Number", blank=True, null=True
    )
    dob = models.CharField(max_length=255, help_text="Date of Birth")
    pob = models.CharField(max_length=255, help_text="Place of Birth")
    provice_place_of_birth = models.CharField(
        max_length=255, help_text="Provice Place Of Birth"
    )
    country = models.CharField(max_length=255)

    education = models.CharField(
        max_length=255, help_text="Highest Formal Education", choices=HIGHEST_EDUCATION
    )
    is_pwd = models.BooleanField(default=False, help_text="Person with disability")
    is_fourps = models.BooleanField(default=False, help_text="4P's Beneficiary")
    is_member_in_ip = models.BooleanField(
        default=False, help_text="Member of an Indigenous Group"
    )
    is_household_head = models.BooleanField(default=False, help_text="Household head")
    is_with_government_id = models.BooleanField(
        default=False, help_text="Government ID"
    )
    is_member_in_any_cooperative = models.BooleanField(
        default=False, help_text="Member in any cooperative"
    )

    member_in_ip_specific = models.CharField(
        max_length=255, help_text="Specific Indigenous Group", null=True, blank=True
    )

    religion = models.CharField(
        max_length=255, choices=RELIGION, help_text="Region you belong"
    )
    civil_status = models.CharField(
        max_length=255, choices=CIVIL_STATUS, help_text="Civil status"
    )
    name_of_spouse_if_married = models.CharField(
        max_length=255, null=True, blank=True, help_text="Name of spouse if married"
    )
    mother_maiden_name = models.CharField(
        max_length=255, help_text="Mother maiden name"
    )

    name_of_household_head = models.CharField(
        max_length=255, help_text="Name of Household", blank=True, null=True
    )
    relationship = models.CharField(
        max_length=255,
        choices=RELATIONSHIP,
        null=True,
        blank=True,
        help_text="Relationship",
    )
    number_of_living_household = models.IntegerField(
        default=0, null=True, blank=True, help_text="No. of living in your household"
    )
    number_of_male = models.IntegerField(
        default=0, null=True, blank=True, help_text="No. of male in your household"
    )
    number_of_female = models.IntegerField(
        default=0, null=True, blank=True, help_text="No. of female in your household"
    )

    type_of_id = models.CharField(
        max_length=255, null=True, blank=True, help_text="What type of ID you have?"
    )
    id_number = models.CharField(
        max_length=255, null=True, blank=True, help_text="Enter your ID number"
    )

    specify_cooperative = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Specify what cooperative you are member with",
    )

    person_to_notify = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self) -> str:
        return self.get_full_name()

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Informations"


class FarmProfile(models.Model):

    MAIN_LIVELIHOOD = (
        ("Farmer", "Farmer"),
        ("Farm Worker", "Farm Worker"),
        ("Agri Youth", "Agri Youth"),
    )

    FARMER = (
        ("Rice", "Rice"),
        ("Corn", "Corn"),
        ("Other Crops", "Other Crops"),
        ("Livestock", "Livestock"),
        ("Poultry", "Poultry"),
    )

    FARM_WORKER = (
        ("Land Preparation", "Land Preparation"),
        ("Planting", "Planting"),
        ("Cultivation", "Cultivation"),
        ("Harvesting", "Harvesting"),
        ("Others", "Others"),
    )

    AGRIYOUTH_WORKER = (
        ("1", "Part of a farming household"),
        ("2", "Attending/attended formal agri-fishery related course"),
        ("3", "Attending/attended non-formal agri-fishery related course"),
        ("4", "Participated in any agricultural activity/program."),
        ("5", "Others"),
    )

    related_to = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    main_livelihood = models.CharField(max_length=255, choices=MAIN_LIVELIHOOD)
    activity_farmer = models.CharField(
        max_length=50, choices=FARMER, null=True, blank=True
    )
    specific_farming_activity = models.CharField(max_length=50, null=True, blank=True)
    activity_farmworker = models.CharField(
        max_length=50, choices=FARM_WORKER, null=True, blank=True
    )
    specific_farmworker_activity = models.CharField(
        max_length=50, null=True, blank=True
    )
    activity_agriyouth = models.CharField(
        max_length=50, choices=AGRIYOUTH_WORKER, null=True, blank=True
    )
    specific_agriyouth_activity = models.CharField(max_length=50, null=True, blank=True)

    status = models.CharField(
        max_length=100,
        default="Pending",
        null=True,
        blank=True,
        choices=(
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Disapproved", "Disapproved"),
        ),
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.related_to.get_full_name()

    class Meta:
        verbose_name = "Farm Profile"
        verbose_name_plural = "Farm Profiles"


class NotificationSent(models.Model):
    sent_to = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    status = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sent_to.get_full_name()} - {self.date_sent}"


class Notification(models.Model):
    message = models.TextField(max_length=500)
    for_municipality = models.ForeignKey(Municpality, on_delete=models.CASCADE)
    farmer_type = models.CharField(
        choices=FarmProfile.MAIN_LIVELIHOOD, max_length=255, default="Farmer"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Message created last {self.date_added}"
