from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def file_size(file):
	limit = 4 * 1024 * 1024
	if file.size > limit:
		raise ValidationError('File too large. Size should not exceed 4 MiB.')


class InformationForm(forms.Form):
	name = forms.CharField(label="Name", max_length=256, required=True)
	email = forms.EmailField(label="Email", max_length=256, required=True)
	phone = PhoneNumberField(label="Phone", max_length=14, required=True)
	full_address = forms.CharField(label="Full Address", max_length=512)
	name_of_university = forms.CharField(label="University", max_length=256, required=True)
	graduation_year = forms.IntegerField(label="Graduation Year", min_value=2015, max_value=2020, required=True)
	cgpa = forms.DecimalField(label="CGPA", min_value=2.0, max_value=4.00, decimal_places=2)
	experience_in_months = forms.IntegerField(label="Experience(Months)", min_value=0, max_value=100)
	current_work_place_name = forms.CharField(label="Currently Working", max_length=100, required=True)
	applying_in = forms.ChoiceField(label="Applying In", choices=(('1', 'Backend'), ('2', 'Mobile')), required=True)
	expected_salary = forms.IntegerField(label="Expected Salary", min_value=15000, max_value=60000, required=True)
	field_buzz_reference = forms.CharField(label="Field Buzz Reference", max_length=256)
	github_project_url = forms.URLField(label="Github Project Url", max_length=512, required=True)
	cv_file = forms.FileField(label="CV", required=True, validators=[FileExtensionValidator(allowed_extensions=['pdf']), file_size])
