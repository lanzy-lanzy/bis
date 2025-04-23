from django.contrib import admin
from .models import Barangay, Person, IdentificationCard


class BarangayAdmin(admin.ModelAdmin):
    list_display = ('name', 'municipality', 'province', 'zip_code')
    search_fields = ('name', 'municipality', 'province')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'gender', 'date_of_birth', 'age', 'barangay')
    list_filter = ('gender', 'civil_status', 'barangay', 'is_active')
    search_fields = ('last_name', 'first_name', 'middle_name', 'address_line1', 'contact_number')
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('last_name', 'first_name', 'middle_name', 'suffix'),
                ('date_of_birth', 'place_of_birth'),
                ('gender', 'civil_status'),
                'religion',
                'profile_picture',
            )
        }),
        ('Contact Information', {
            'fields': (
                'contact_number',
            )
        }),
        ('Address Information', {
            'fields': (
                'address_line1',
                'address_line2',
                'postal_code',
            )
        }),
        ('System Fields', {
            'fields': (
                'is_active',
                'barangay',
                'user',
            )
        }),
    )
    readonly_fields = ('age',)


class IdentificationCardAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'person', 'date_issued', 'valid_until', 'is_active', 'is_valid')
    list_filter = ('is_active', 'date_issued')
    search_fields = ('id_number', 'person__last_name', 'person__first_name')


# Register models
admin.site.register(Barangay, BarangayAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(IdentificationCard, IdentificationCardAdmin)
