from django import forms
from .models import StoredData  # Assuming StoredData model in data_storage

class DynamicReportForm(forms.Form):
    filters = forms.CharField()  # Assuming other filter fields exist
    data_points = forms.MultipleChoiceField(
        choices=[(field.name, field.verbose_name) for field in StoredData._meta.get_fields()
                 if not field.is_relation],  # Exclude relations
        widget=forms.CheckboxSelectMultiple
    )


class ReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=True)
    end_date = forms.DateField(label='End Date', required=True)
    filename = forms.CharField(label='Filename (contains)', required=False)  # Optional filtering
    source = forms.CharField(label='Source (contains)', required=False)  # Optional filtering
    status = forms.ChoiceField(
        label='Status',
        choices=[('', 'All'), ('uploaded', 'Uploaded'), ('processing', 'Processing'), ('failed', 'Processing Failed')],
        required=False,  # Optional filtering
    )
    data_points = forms.MultipleChoiceField(
        label='Data Points',
        choices=[
            (field.name, field.verbose_name) for field in StoredData._meta.fields
                if field.name not in ['id', 'filename', 'upload_date', 'checksum', 'processing_details']  # Exclude irrelevant fields
                and field.get_internal_type() in ['IntegerField', 'FloatField']  # Focus on numerical data
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    # Add additional fields based on your data and insights (e.g., custom numerical fields)
    # ...
