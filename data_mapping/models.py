from django.db import models
from .utils import *

class Mapping(models.Model):
    # Data source information
    source = models.CharField(max_length=255)  # Source system or file type
    source_filename = models.CharField(max_length=255, blank=True)  # Optional filename

    # Mapping details
    field_name_source = models.CharField(max_length=255)  # Field name in source data
    field_name_target = models.CharField(max_length=255)  # Field name in target data
    data_type = models.CharField(max_length=25, choices=(
        ('STRING', 'String'),
        ('INTEGER', 'Integer'),
        ('FLOAT', 'Float'),
        ('DATE', 'Date'),
        ('DATETIME', 'Datetime'),
        ('BOOLEAN', 'Boolean'),
        ('EMAIL', 'Email'),  
        ('URL', 'URL'),  
        ('JSON', 'JSON'),
        ('CURRENCY', 'Currency'),
        ('PHONE_NUMBER', 'Phone Number'),
        ('POSTAL_CODE', 'Postal Code'),
        ('CSV', 'CSV'),
        ('BASE64', 'Base64 Encoded'),
        ('COLOR', 'Color'),  
    ))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, blank=True)  # Optional, calculated field
    formatted_name = models.CharField(max_length=200, blank=True)  # Optional, calculated field
    transformation_rule = models.TextField(blank=True)  # Optional transformation logic
    target_format = models.CharField(max_length=255, blank=True)  # Specify target format for dates, etc.
    default_value = models.TextField(blank=True)  # Set a default value for missing source data
    description = models.TextField(blank=True)  # Provide a description for the mapping
    currency_code = models.CharField(max_length=10, blank=True)  # Optional field for specifying currency (e.g., USD)
    delimiter = models.CharField(max_length=5, blank=True, default=',')  # Optional field for delimiter (e.g., ';' for semicolon-separated)
    color_format = models.CharField(max_length=10, blank=True, choices=(  # Optional: Specify color format (e.g., HEX, RGB)
        ('HEX', 'HEX Code'),
        ('RGB', 'RGB Values'),
    ))

    def __str__(self):
        return f"Mapping: {self.source} - {self.field_name_source} to {self.field_name_target}"

    def save(self, *args, **kwargs):
        self.full_name = combine_fields(self.first_name, self.last_name)
        self.formatted_name = capitalize_first_letter(self.full_name)
        super().save(*args, **kwargs)  # Call the original save method

    class Meta:
        unique_together = ('source', 'field_name_source')  # Enforce uniqueness for the pair