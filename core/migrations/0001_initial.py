# Generated by Django 4.2.17 on 2025-04-21 01:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Barangay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('municipality', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('population', models.PositiveIntegerField(blank=True, null=True)),
                ('land_area', models.DecimalField(blank=True, decimal_places=2, help_text='Land area in square kilometers', max_digits=10, null=True)),
                ('date_established', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='barangay_logos/')),
            ],
            options={
                'verbose_name_plural': 'Barangays',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('suffix', models.CharField(blank=True, help_text='Jr., Sr., III, etc.', max_length=10)),
                ('nickname', models.CharField(blank=True, max_length=50)),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('civil_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced'), ('SP', 'Separated'), ('L', 'Live-in')], max_length=2)),
                ('citizenship', models.CharField(default='Filipino', max_length=50)),
                ('religion', models.CharField(blank=True, max_length=100)),
                ('ethnicity', models.CharField(blank=True, max_length=100)),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'), ('UNK', 'Unknown')], default='UNK', max_length=3)),
                ('contact_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('facebook', models.CharField(blank=True, help_text='Facebook username or profile URL', max_length=100)),
                ('address_line1', models.CharField(help_text='House/Lot/Unit No., Building Name, Block, Street', max_length=255)),
                ('address_line2', models.CharField(blank=True, help_text='Subdivision, Village, Zone, Sitio, Purok', max_length=255)),
                ('postal_code', models.CharField(max_length=10)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('educational_attainment', models.CharField(blank=True, choices=[('N', 'None'), ('E', 'Elementary'), ('HS', 'High School'), ('V', 'Vocational'), ('C', 'College'), ('G', 'Graduate'), ('PG', 'Post-Graduate')], max_length=2)),
                ('school_name', models.CharField(blank=True, max_length=255)),
                ('course', models.CharField(blank=True, max_length=255)),
                ('year_graduated', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
                ('occupation', models.CharField(blank=True, max_length=255)),
                ('employer', models.CharField(blank=True, max_length=255)),
                ('employer_address', models.CharField(blank=True, max_length=255)),
                ('monthly_income', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('skills', models.TextField(blank=True, help_text='Comma-separated list of skills')),
                ('sss_no', models.CharField(blank=True, max_length=20, verbose_name='SSS Number')),
                ('tin_no', models.CharField(blank=True, max_length=20, verbose_name='TIN Number')),
                ('philhealth_no', models.CharField(blank=True, max_length=20, verbose_name='PhilHealth Number')),
                ('pagibig_no', models.CharField(blank=True, max_length=20, verbose_name='Pag-IBIG Number')),
                ('voters_id', models.CharField(blank=True, max_length=30, verbose_name="Voter's ID")),
                ('precinct_no', models.CharField(blank=True, max_length=30, verbose_name='Precinct Number')),
                ('height', models.DecimalField(blank=True, decimal_places=2, help_text='Height in centimeters', max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='Weight in kilograms', max_digits=5, null=True)),
                ('pwd', models.BooleanField(default=False, verbose_name='Person with Disability')),
                ('pwd_id', models.CharField(blank=True, max_length=30, verbose_name='PWD ID Number')),
                ('pwd_details', models.TextField(blank=True, verbose_name='Disability Details')),
                ('medical_conditions', models.TextField(blank=True)),
                ('allergies', models.TextField(blank=True)),
                ('medications', models.TextField(blank=True)),
                ('father_name', models.CharField(blank=True, max_length=255)),
                ('father_occupation', models.CharField(blank=True, max_length=255)),
                ('mother_name', models.CharField(blank=True, max_length=255)),
                ('mother_occupation', models.CharField(blank=True, max_length=255)),
                ('spouse_name', models.CharField(blank=True, max_length=255)),
                ('spouse_occupation', models.CharField(blank=True, max_length=255)),
                ('number_of_children', models.PositiveIntegerField(default=0)),
                ('household_head', models.BooleanField(default=False)),
                ('household_members', models.PositiveIntegerField(default=1, help_text='Total number of people in the household')),
                ('emergency_contact_name', models.CharField(blank=True, max_length=255)),
                ('emergency_contact_relationship', models.CharField(blank=True, max_length=100)),
                ('emergency_contact_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('emergency_contact_address', models.CharField(blank=True, max_length=255)),
                ('years_of_residency', models.PositiveIntegerField(default=0, help_text='Number of years living in the barangay')),
                ('resident_status', models.CharField(default='Permanent', help_text='Permanent, Temporary, etc.', max_length=50)),
                ('homeowner', models.BooleanField(default=False)),
                ('renting', models.BooleanField(default=False)),
                ('living_with_relatives', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deceased', models.BooleanField(default=False)),
                ('date_of_death', models.DateField(blank=True, null=True)),
                ('cause_of_death', models.CharField(blank=True, max_length=255)),
                ('remarks', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='resident_photos/')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='resident_qrcodes/')),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('barangay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residents', to='core.barangay')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'People',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IdentificationCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=50, unique=True)),
                ('date_issued', models.DateField()),
                ('valid_until', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('issued_by', models.CharField(max_length=255)),
                ('purpose', models.CharField(blank=True, max_length=255)),
                ('remarks', models.TextField(blank=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_cards', to='core.person')),
            ],
            options={
                'verbose_name_plural': 'Identification Cards',
            },
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('household_code', models.CharField(max_length=50, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('economic_status', models.CharField(blank=True, help_text='e.g., Low Income, Middle Income, etc.', max_length=50)),
                ('monthly_income', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('house_ownership', models.CharField(blank=True, help_text='Owned, Rented, etc.', max_length=50)),
                ('house_type', models.CharField(blank=True, help_text='Concrete, Wood, etc.', max_length=50)),
                ('toilet_type', models.CharField(blank=True, max_length=50)),
                ('water_source', models.CharField(blank=True, max_length=50)),
                ('electricity', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('barangay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='households', to='core.barangay')),
                ('head', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_household', to='core.person')),
                ('members', models.ManyToManyField(related_name='household', to='core.person')),
            ],
            options={
                'verbose_name_plural': 'Households',
            },
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField()),
                ('record_type', models.CharField(help_text='Checkup, Vaccination, Treatment, etc.', max_length=100)),
                ('healthcare_provider', models.CharField(blank=True, max_length=255)),
                ('facility', models.CharField(blank=True, max_length=255)),
                ('diagnosis', models.TextField(blank=True)),
                ('treatment', models.TextField(blank=True)),
                ('medications', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='core.person')),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', models.CharField(choices=[('SP', 'Spouse'), ('CH', 'Child'), ('PA', 'Parent'), ('SI', 'Sibling'), ('GP', 'Grandparent'), ('GC', 'Grandchild'), ('AU', 'Aunt/Uncle'), ('NI', 'Niece/Nephew'), ('CO', 'Cousin'), ('IL', 'In-law'), ('OT', 'Other')], max_length=2)),
                ('notes', models.TextField(blank=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_relationships', to='core.person')),
                ('relative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_to', to='core.person')),
            ],
            options={
                'verbose_name_plural': 'Family Members',
            },
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('employer_address', models.CharField(blank=True, max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('current_job', models.BooleanField(default=False)),
                ('job_description', models.TextField(blank=True)),
                ('salary_range', models.CharField(blank=True, max_length=100)),
                ('reason_for_leaving', models.TextField(blank=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_history', to='core.person')),
            ],
            options={
                'verbose_name_plural': 'Employment Histories',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='EducationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('PR', 'Preschool'), ('EL', 'Elementary'), ('JH', 'Junior High School'), ('SH', 'Senior High School'), ('VO', 'Vocational'), ('CO', 'College'), ('GR', 'Graduate School'), ('PG', 'Post-Graduate')], max_length=2)),
                ('school_name', models.CharField(max_length=255)),
                ('school_address', models.CharField(blank=True, max_length=255)),
                ('field_of_study', models.CharField(blank=True, max_length=255)),
                ('year_started', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
                ('year_ended', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
                ('graduated', models.BooleanField(default=False)),
                ('honors', models.CharField(blank=True, max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education_records', to='core.person')),
            ],
            options={
                'ordering': ['-year_started'],
            },
        ),
        migrations.CreateModel(
            name='Vaccination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=255)),
                ('dose_number', models.PositiveIntegerField(default=1)),
                ('date_administered', models.DateField()),
                ('administered_by', models.CharField(blank=True, max_length=255)),
                ('facility', models.CharField(blank=True, max_length=255)),
                ('batch_number', models.CharField(blank=True, max_length=100)),
                ('next_dose_date', models.DateField(blank=True, null=True)),
                ('side_effects', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccinations', to='core.person')),
            ],
            options={
                'ordering': ['-date_administered'],
                'unique_together': {('person', 'vaccine_name', 'dose_number')},
            },
        ),
        migrations.CreateModel(
            name='PersonSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency', models.CharField(choices=[('BG', 'Beginner'), ('IT', 'Intermediate'), ('AD', 'Advanced'), ('EX', 'Expert')], default='IT', max_length=2)),
                ('years_of_experience', models.PositiveIntegerField(default=0)),
                ('certification', models.CharField(blank=True, max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills_set', to='core.person')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='core.skill')),
            ],
            options={
                'unique_together': {('person', 'skill')},
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['last_name', 'first_name'], name='core_person_last_na_0bc83a_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['date_of_birth'], name='core_person_date_of_ef7045_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['barangay'], name='core_person_baranga_9313b3_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='familymember',
            unique_together={('person', 'relative')},
        ),
    ]
