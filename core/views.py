from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
import json
import traceback
from .models import Barangay, Person, IdentificationCard
from .forms import PersonForm, PersonSearchForm, BarangayForm, BarangaySearchForm, IdentificationCardForm, IdentificationCardSearchForm

def home(request):
    # Redirect to dashboard
    return redirect('dashboard')

def dashboard(request):
    # Get counts for dashboard cards
    barangay_count = Barangay.objects.count()
    resident_count = Person.objects.count()
    idcard_count = IdentificationCard.objects.count()

    # Get gender statistics
    gender_stats = {
        'M': Person.objects.filter(gender='M').count(),
        'F': Person.objects.filter(gender='F').count(),
        'O': Person.objects.filter(gender='O').count(),
    }

    # Get civil status statistics
    civil_status_counts = Person.objects.values('civil_status').annotate(count=Count('id'))
    civil_status_stats = {}
    for status in Person.CIVIL_STATUS_CHOICES:
        civil_status_stats[status[1]] = 0

    for item in civil_status_counts:
        for choice in Person.CIVIL_STATUS_CHOICES:
            if item['civil_status'] == choice[0]:
                civil_status_stats[choice[1]] = item['count']

    context = {
        'barangay_count': barangay_count,
        'resident_count': resident_count,
        'idcard_count': idcard_count,
        'gender_stats': gender_stats,
        'civil_status_stats': civil_status_stats,
        'now': timezone.now(),
    }

    return render(request, 'dashboard/overview.html', context)

def people_list(request):
    people = Person.objects.all().select_related('barangay')
    search_form = PersonSearchForm()
    return render(request, 'dashboard/people.html', {
        'people': people,
        'search_form': search_form
    })

def person_search(request):
    form = PersonSearchForm(request.POST)
    people = Person.objects.all().select_related('barangay')

    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        barangay = form.cleaned_data.get('barangay')
        gender = form.cleaned_data.get('gender')
        civil_status = form.cleaned_data.get('civil_status')

        if search_query:
            people = people.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(middle_name__icontains=search_query) |
                Q(contact_number__icontains=search_query) |
                Q(barangay__name__icontains=search_query)
            )

        if barangay:
            people = people.filter(barangay=barangay)

        if gender:
            people = people.filter(gender=gender)

        if civil_status:
            people = people.filter(civil_status=civil_status)

    html = render_to_string(
        'dashboard/includes/people_table.html',
        {'people': people}
    )
    return HttpResponse(html)

def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            messages.success(request, f'Resident {person.full_name()} has been created successfully.')
            return redirect('people')
    else:
        form = PersonForm()

    return render(request, 'dashboard/person_form.html', {
        'form': form,
        'title': 'Add New Resident',
        'submit_text': 'Create Resident',
        'form_id': 'createPersonForm',
        'is_create': True
    })

def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    id_cards = person.id_cards.all()

    return render(request, 'dashboard/person_detail.html', {
        'person': person,
        'id_cards': id_cards
    })

def person_update(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, f'Resident {person.full_name()} has been updated successfully.')
            return redirect('person_detail', pk=person.pk)
    else:
        form = PersonForm(instance=person)

    return render(request, 'dashboard/person_form.html', {
        'form': form,
        'title': f'Edit Resident: {person.full_name()}',
        'submit_text': 'Update Resident',
        'form_id': 'updatePersonForm',
        'is_create': False,
        'person': person
    })

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        person_name = person.full_name()
        person.delete()
        messages.success(request, f'Resident {person_name} has been deleted successfully.')
        return redirect('people')

    return render(request, 'dashboard/person_confirm_delete.html', {
        'person': person
    })

def barangay_list(request):
    barangays = Barangay.objects.all()
    search_form = BarangaySearchForm()

    # Get unique province count
    province_count = Barangay.objects.values('province').distinct().count()

    # Get province data for chart
    province_data = []
    provinces = Barangay.objects.values('province').annotate(count=Count('id')).order_by('province')
    for province in provinces:
        province_data.append({
            'name': province['province'],
            'count': province['count']
        })

    return render(request, 'dashboard/barangays.html', {
        'barangays': barangays,
        'search_form': search_form,
        'province_count': province_count,
        'province_data': province_data
    })

def barangay_search(request):
    form = BarangaySearchForm(request.POST)
    barangays = Barangay.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        province_filter = form.cleaned_data.get('province')

        if search_query:
            barangays = barangays.filter(
                Q(name__icontains=search_query) |
                Q(municipality__icontains=search_query) |
                Q(province__icontains=search_query) |
                Q(zip_code__icontains=search_query)
            )

        if province_filter:
            barangays = barangays.filter(province__icontains=province_filter)

    html = render_to_string(
        'dashboard/includes/barangays_table.html',
        {'barangays': barangays}
    )
    return HttpResponse(html)

def barangay_create(request):
    if request.method == 'POST':
        form = BarangayForm(request.POST)
        if form.is_valid():
            barangay = form.save()
            messages.success(request, f'Barangay {barangay.name} has been created successfully.')
            return redirect('barangays')
    else:
        form = BarangayForm()

    return render(request, 'dashboard/barangay_form.html', {
        'form': form,
        'title': 'Add New Barangay',
        'submit_text': 'Create Barangay',
        'form_id': 'createBarangayForm',
        'is_create': True
    })

def barangay_detail(request, pk):
    barangay = get_object_or_404(Barangay, pk=pk)
    residents = barangay.residents.all()
    resident_count = residents.count()

    # Get gender statistics for this barangay
    gender_stats = {
        'M': residents.filter(gender='M').count(),
        'F': residents.filter(gender='F').count(),
        'O': residents.filter(gender='O').count(),
    }

    return render(request, 'dashboard/barangay_detail.html', {
        'barangay': barangay,
        'residents': residents[:10],  # Limit to 10 residents for the preview
        'resident_count': resident_count,
        'gender_stats': gender_stats
    })

def barangay_update(request, pk):
    barangay = get_object_or_404(Barangay, pk=pk)

    if request.method == 'POST':
        form = BarangayForm(request.POST, instance=barangay)
        if form.is_valid():
            form.save()
            messages.success(request, f'Barangay {barangay.name} has been updated successfully.')
            return redirect('barangay_detail', pk=barangay.pk)
    else:
        form = BarangayForm(instance=barangay)

    return render(request, 'dashboard/barangay_form.html', {
        'form': form,
        'title': f'Edit Barangay: {barangay.name}',
        'submit_text': 'Update Barangay',
        'form_id': 'updateBarangayForm',
        'is_create': False,
        'barangay': barangay
    })

def barangay_delete(request, pk):
    barangay = get_object_or_404(Barangay, pk=pk)
    resident_count = barangay.residents.count()

    if request.method == 'POST':
        if resident_count > 0:
            messages.error(request, f'Cannot delete Barangay {barangay.name} because it has {resident_count} residents. Please reassign or delete these residents first.')
            return redirect('barangay_detail', pk=barangay.pk)

        barangay_name = barangay.name
        barangay.delete()
        messages.success(request, f'Barangay {barangay_name} has been deleted successfully.')
        return redirect('barangays')

    return render(request, 'dashboard/barangay_confirm_delete.html', {
        'barangay': barangay,
        'resident_count': resident_count
    })

def id_card_list(request):
    id_cards = IdentificationCard.objects.all().select_related('person')
    search_form = IdentificationCardSearchForm()

    # Check if we need to auto-open the print modal
    # Only pass print_card_id if it's explicitly provided in the URL
    context = {
        'id_cards': id_cards,
        'search_form': search_form,
    }

    # Only add print_card_id to context if it's explicitly provided
    if 'print' in request.GET and request.GET.get('print'):
        context['print_card_id'] = request.GET.get('print')

    return render(request, 'dashboard/id-cards-new.html', context)

def id_card_search(request):
    form = IdentificationCardSearchForm(request.POST)
    id_cards = IdentificationCard.objects.all().select_related('person')

    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        status = form.cleaned_data.get('status')

        if search_query:
            id_cards = id_cards.filter(
                Q(id_number__icontains=search_query) |
                Q(person__first_name__icontains=search_query) |
                Q(person__last_name__icontains=search_query)
            )

        if status == 'active':
            id_cards = id_cards.filter(is_active=True)
        elif status == 'expired':
            id_cards = id_cards.filter(is_active=False)

    html = render_to_string(
        'dashboard/includes/id_cards_table.html',
        {'id_cards': id_cards}
    )
    return HttpResponse(html)

def id_card_create(request):
    person_id = request.GET.get('person_id')
    initial_data = {}
    person = None

    if person_id:
        person = get_object_or_404(Person, pk=person_id)
        initial_data['person'] = person

    if request.method == 'POST':
        form = IdentificationCardForm(request.POST)
        if form.is_valid():
            id_card = form.save()
            messages.success(request, f'ID Card {id_card.id_number} has been issued successfully.')

            # If this was created from a person's detail page, redirect back there
            if 'person_id' in request.GET:
                return redirect('person_detail', pk=request.GET['person_id'])
            return redirect('id_cards')
    else:
        form = IdentificationCardForm(initial=initial_data)

    context = {
        'form': form,
        'title': 'Issue New ID Card',
        'submit_text': 'Issue ID Card',
        'form_id': 'createIdCardForm',
        'is_create': True
    }

    if person:
        context['subtitle'] = f'for {person.full_name()}'

    return render(request, 'dashboard/id_card_form.html', context)

def id_card_detail(request, pk):
    id_card = get_object_or_404(IdentificationCard, pk=pk)

    return render(request, 'dashboard/id_card_detail.html', {
        'id_card': id_card
    })

def id_card_update(request, pk):
    id_card = get_object_or_404(IdentificationCard, pk=pk)

    if request.method == 'POST':
        form = IdentificationCardForm(request.POST, instance=id_card)
        if form.is_valid():
            form.save()
            messages.success(request, f'ID Card {id_card.id_number} has been updated successfully.')
            return redirect('id_card_detail', pk=id_card.pk)
    else:
        form = IdentificationCardForm(instance=id_card)

    return render(request, 'dashboard/id_card_form.html', {
        'form': form,
        'title': f'Edit ID Card: {id_card.id_number}',
        'submit_text': 'Update ID Card',
        'form_id': 'updateIdCardForm',
        'is_create': False,
        'id_card': id_card
    })

def id_card_delete(request, pk):
    id_card = get_object_or_404(IdentificationCard, pk=pk)

    if request.method == 'POST':
        id_number = id_card.id_number
        person = id_card.person
        id_card.delete()
        messages.success(request, f'ID Card {id_number} has been deleted successfully.')

        # Check if we should redirect to the person detail page
        if 'next' in request.GET and request.GET['next'] == 'person':
            return redirect('person_detail', pk=person.pk)
        return redirect('id_cards')

    return render(request, 'dashboard/id_card_confirm_delete.html', {
        'id_card': id_card
    })

def id_card_data(request, pk):
    """API endpoint to get ID card data for printing"""
    id_card = get_object_or_404(IdentificationCard, pk=pk)
    person = id_card.person

    # Format the address
    address = person.address_line1
    if person.address_line2:
        address += f", {person.address_line2}"

    # Check if the card is valid
    is_valid = id_card.is_valid()

    # Format the barangay address
    barangay_address = f"{person.barangay.name}, Dumingag, Zamboanga del Sur"

    # Get position or default to BERT Member
    position = getattr(person, 'position', None) or 'BERT Member'

    # Calculate age from date of birth
    from datetime import date
    today = date.today()
    age = today.year - person.date_of_birth.year - ((today.month, today.day) < (person.date_of_birth.month, person.date_of_birth.day))

    # Get static file URLs
    from django.templatetags.static import static

    # Prepare the data
    data = {
        'id_number': id_card.id_number,
        'person_name': person.full_name(),
        'barangay': person.barangay.name,
        'barangay_address': barangay_address,
        'position': position,
        'date_of_birth': person.date_of_birth.strftime('%B %d, %Y'),
        'age': age,
        'sex': getattr(person, 'get_gender_display', lambda: 'Not specified')(),
        'civil_status': getattr(person, 'get_civil_status_display', lambda: 'Not specified')(),
        'address': address,
        'contact_number': person.contact_number or 'Not provided',
        'date_issued': id_card.date_issued.strftime('%B %d, %Y'),
        'valid_until': id_card.valid_until.strftime('%B %d, %Y'),
        'is_valid': is_valid,
        'initials': f"{person.first_name[0]}{person.last_name[0]}",
        'profile_picture': person.profile_picture.url if person.profile_picture else None,
        'blood_type': getattr(person, 'blood_type', None) or 'Not specified',
        'emergency_contact': getattr(person, 'emergency_contact', None) or person.contact_number or 'Not provided',
        # Add height and weight if available
        'height': f"{getattr(person, 'height', None)} cm" if getattr(person, 'height', None) else None,
        'weight': f"{getattr(person, 'weight', None)} kg" if getattr(person, 'weight', None) else None,
        # Add static file URLs
        'dumingag_logo_url': request.build_absolute_uri(static('images/dumingag-logo.png')),
        'drr_logo_url': request.build_absolute_uri(static('images/drr-logo.png')),
        'static_url': request.build_absolute_uri(static(''))
    }

    # If format=html is specified, render the HTML template
    if request.GET.get('format') == 'html':
        try:
            # Try to render the template with the data
            from django.template.loader import render_to_string
            from django.http import HttpResponse

            # Add debug information
            import json
            print(f"Rendering ID card template with data: {json.dumps(data, default=str)}")

            html_content = render_to_string('components/id_card_printable.html', data)

            # Log the length of the rendered HTML for debugging
            print(f"Rendered HTML length: {len(html_content)}")

            response = HttpResponse(html_content)
            response['Content-Type'] = 'text/html; charset=utf-8'
            return response
        except Exception as e:
            # Log the error and return a helpful error message
            import traceback
            print(f"Error rendering ID card template: {e}")
            print(traceback.format_exc())
            return HttpResponse(f"<div class='error'>Error rendering ID card: {e}</div>", status=500)

    # If format=json is specified or no format is specified, return JSON data
    from django.http import JsonResponse
    return JsonResponse(data)

def id_card_print(request, pk):
    """Dedicated page for printing an ID card"""
    # Verify the ID card exists but we don't need to use it directly
    get_object_or_404(IdentificationCard, pk=pk)

    # Use the standalone template for better printing
    return render(request, 'dashboard/id_card_print_standalone.html', {
        'id_card_id': pk
    })

def id_card_direct_print(request, pk):
    """Direct print page that renders the ID card without JavaScript"""
    id_card = get_object_or_404(IdentificationCard, pk=pk)
    person = id_card.person

    # Format the address
    address = person.address_line1
    if person.address_line2:
        address += f", {person.address_line2}"

    # Format the barangay address
    barangay_address = f"{person.barangay.name}, Dumingag, Zamboanga del Sur"

    # Get position or default to BERT Member
    position = getattr(person, 'position', None) or 'BERT Member'

    # Calculate age from date of birth
    from datetime import date
    today = date.today()
    age = today.year - person.date_of_birth.year - ((today.month, today.day) < (person.date_of_birth.month, person.date_of_birth.day))

    # Get static file URLs
    from django.templatetags.static import static

    # Prepare the context
    context = {
        'id_card': id_card,
        'id_number': id_card.id_number,
        'person_name': person.full_name(),
        'barangay': person.barangay.name,
        'barangay_address': barangay_address,
        'position': position,
        'date_of_birth': person.date_of_birth.strftime('%B %d, %Y'),
        'age': age,
        'sex': getattr(person, 'get_gender_display', lambda: 'Not specified')(),
        'civil_status': getattr(person, 'get_civil_status_display', lambda: 'Not specified')(),
        'address': address,
        'contact_number': person.contact_number or 'Not provided',
        'date_issued': id_card.date_issued.strftime('%B %d, %Y'),
        'valid_until': id_card.valid_until.strftime('%B %d, %Y'),
        'is_valid': id_card.is_valid(),
        'initials': f"{person.first_name[0]}{person.last_name[0]}",
        'profile_picture': person.profile_picture.url if person.profile_picture else None,
        'blood_type': getattr(person, 'blood_type', None) or 'Not specified',
        'emergency_contact': getattr(person, 'emergency_contact', None) or person.contact_number or 'Not provided',
        # Add height and weight if available
        'height': f"{getattr(person, 'height', None)} cm" if getattr(person, 'height', None) else None,
        'weight': f"{getattr(person, 'weight', None)} kg" if getattr(person, 'weight', None) else None,
        # Add static file URLs
        'dumingag_logo_url': request.build_absolute_uri(static('images/dumingag-logo.png')),
        'drr_logo_url': request.build_absolute_uri(static('images/drr-logo.png')),
        'static_url': request.build_absolute_uri(static(''))
    }

    return render(request, 'dashboard/id_card_direct_print.html', context)
