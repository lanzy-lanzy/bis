from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Barangay(models.Model):
    """Model representing a barangay (smallest administrative division in the Philippines)"""
    name = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)


    class Meta:
        verbose_name_plural = 'Barangays'

    def __str__(self):
        return f"{self.name}, {self.municipality}, {self.province}"


class Person(models.Model):
    """Base model for storing comprehensive individual information"""
    # Basic Personal Information
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    CIVIL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('D', 'Divorced'),
        ('SP', 'Separated'),
        ('L', 'Live-in'),
    ]



    # Unique identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, related_name='residents')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')

    # Personal Information
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=10, blank=True, help_text='Jr., Sr., III, etc.')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, help_text='Profile picture of the person')


    # Birth Information
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True, editable=False)

    # Demographics
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    civil_status = models.CharField(max_length=2, choices=CIVIL_STATUS_CHOICES)
    religion = models.CharField(max_length=100, blank=True)
    # Contact Information
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


    # Address Information
    address_line1 = models.CharField(max_length=255, help_text='House/Lot/Unit No., Building Name, Block, Street')
    address_line2 = models.CharField(max_length=255, blank=True, help_text='Subdivision, Village, Zone, Sitio, Purok')
    postal_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'People'
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['date_of_birth']),
            models.Index(fields=['barangay']),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}"

    def save(self, *args, **kwargs):
        # Calculate age based on date of birth
        if self.date_of_birth:
            today = timezone.now().date()
            born = self.date_of_birth
            self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        super().save(*args, **kwargs)

    def full_name(self):
        """Return the person's full name."""
        if self.middle_name:
            middle_initial = f" {self.middle_name[0]}."
        else:
            middle_initial = " "

        full_name = f"{self.first_name}{middle_initial}{self.last_name}"
        if self.suffix:
            full_name = f"{full_name}, {self.suffix}"
        return full_name




class IdentificationCard(models.Model):
    """Model for tracking barangay-issued ID cards"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='id_cards')
    id_number = models.CharField(max_length=50, unique=True)
    date_issued = models.DateField()
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)
    issued_by = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Identification Cards'

    def __str__(self):
        return f"{self.id_number} - {self.person}"

    def is_valid(self):
        return self.is_active and self.valid_until >= timezone.now().date()


