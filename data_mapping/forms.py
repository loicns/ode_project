from django import forms
from django.core.exceptions import ValidationError
from .models import Mapping
import re


class MappingForm(forms.ModelForm):
    class Meta:
        model = Mapping
        fields = '__all__'

    def clean_field_name_source(self, value):
        # Check for unique field combination (source + field_name_source)
        source = self.cleaned_data.get('source')
        if Mapping.objects.filter(source=source, field_name_source=value).exists():
            raise forms.ValidationError(
                'A mapping for this source already uses the field name "%s". Please choose a unique field name.'
                % value
            )
        return value

    def clean_data_type(self, value):
        # Optional: Validate data type selection based on other fields (e.g., email format for 'EMAIL')
        if value == 'EMAIL' and not re.match(r"[^@]+@[^@]+\.[^@]+", self.cleaned_data.get('field_name_source')):
            raise forms.ValidationError('Please select "String" data type for non-email fields.')
        return value

    def clean(self):
        cleaned_data = super().clean()

        # Additional validation for specific fields (optional):
        if cleaned_data.get('data_type') == 'URL':
            # Validate URL format using a library (e.g., validators.url)
            try:
                import validators
                if not validators.url(cleaned_data.get('field_name_source')):
                    raise forms.ValidationError('Please enter a valid URL.')
            except ImportError:
                # Handle import error gracefully (e.g., log a warning)
                pass

        # Customize validation for other data types (e.g., date, currency) as needed

        return cleaned_data
