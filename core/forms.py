from django import forms
from .models import Person, Barangay, IdentificationCard

class BarangayForm(forms.ModelForm):
    """Form for creating and updating Barangay records"""

    class Meta:
        model = Barangay
        fields = ['name', 'municipality', 'province', 'zip_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'province': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
        }

class BarangaySearchForm(forms.Form):
    """Form for searching Barangay records"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Search by name, municipality, or province',
            'hx-post': '/dashboard/barangays/search/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#barangays-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

    province = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Filter by province',
            'hx-post': '/dashboard/barangays/search/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#barangays-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

class PersonForm(forms.ModelForm):
    """Form for creating and updating Person records"""

    # Override the barangay field to use a select widget
    barangay = forms.ModelChoiceField(
        queryset=Barangay.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'})
    )

    # Override date field to use date input
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )

    class Meta:
        model = Person
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix',
            'date_of_birth', 'place_of_birth', 'gender', 'civil_status',
            'religion', 'contact_number', 'address_line1', 'address_line2',
            'postal_code', 'barangay', 'profile_picture', 'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'suffix': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'gender': forms.Select(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'civil_status': forms.Select(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'religion': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        }

class PersonSearchForm(forms.Form):
    """Form for searching Person records"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Search by name, barangay, or contact number',
            'hx-post': '/dashboard/people/search/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#people-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

    barangay = forms.ModelChoiceField(
        queryset=Barangay.objects.all(),
        required=False,
        empty_label="All Barangays",
        widget=forms.Select(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'hx-post': '/dashboard/people/search/',
            'hx-trigger': 'change',
            'hx-target': '#people-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

    gender = forms.ChoiceField(
        choices=[('', 'All Genders')] + Person.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'hx-post': '/dashboard/people/search/',
            'hx-trigger': 'change',
            'hx-target': '#people-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

    civil_status = forms.ChoiceField(
        choices=[('', 'All Civil Status')] + Person.CIVIL_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'hx-post': '/dashboard/people/search/',
            'hx-trigger': 'change',
            'hx-target': '#people-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

class IdentificationCardForm(forms.ModelForm):
    """Form for creating and updating ID Card records"""

    # Override date fields to use date input
    date_issued = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )

    valid_until = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'
        })
    )

    # Override the person field to use a select widget
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'})
    )

    class Meta:
        model = IdentificationCard
        fields = ['person', 'id_number', 'date_issued', 'valid_until', 'is_active', 'issued_by', 'purpose', 'remarks']
        widgets = {
            'id_number': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'issued_by': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        }

class IdentificationCardSearchForm(forms.Form):
    """Form for searching ID Card records"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'Search by ID number or person name',
            'hx-post': '/dashboard/id-cards/search/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#id-cards-table',
            'hx-indicator': '.htmx-indicator'
        })
    )

    status = forms.ChoiceField(
        choices=[('', 'All Status'), ('active', 'Active'), ('expired', 'Expired')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'hx-post': '/dashboard/id-cards/search/',
            'hx-trigger': 'change',
            'hx-target': '#id-cards-table',
            'hx-indicator': '.htmx-indicator'
        })
    )
