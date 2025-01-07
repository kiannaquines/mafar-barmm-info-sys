from django.contrib import admin
from main.models import *

admin.site.register(FarmProfile)
admin.site.register(PersonalInformation)
admin.site.register(NotificationSent)
admin.site.register(Notification)

class BarangayAdmin(admin.ModelAdmin):
    list_display = ('barangay', 'municipality')
    list_display_links = ('barangay',)
    list_editable = ('municipality',)
    search_fields = ('barangay',)
    list_filter = ('municipality',)
    ordering = ('municipality', 'barangay')
    list_per_page = 20
    save_on_top = True
    save_as_new = True
    show_full_result_count = False

admin.site.register(Barangay, BarangayAdmin)

admin.site.register(Municpality)