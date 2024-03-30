import chardet
from django.core.files.uploadedfile import UploadedFile
from .models import Upload
from celery import shared_task
import pandas as pd
from data_mapping.models import Mapping

@shared_task
def parse_uploaded_file(upload_id, uploaded_file: UploadedFile):
    """Parses the uploaded file and saves the results or error message."""
    try:
        upload = Upload.objects.get(pk=upload_id)
        if uploaded_file.name.endswith('.csv'):
             # Detect the file encoding
            result = chardet.detect(uploaded_file.read())
            uploaded_file.seek(0)  # reset file pointer to the beginning

            # Load CSV using Pandas with the detected encoding
            df = pd.read_csv(uploaded_file, encoding=result['encoding'])

            # ... Process data from the DataFrame (e.g., save to database)
        else:
            print(f"Unsupported file type: {uploaded_file.name}")
    except Upload.DoesNotExist as e:
        print(f"Error parsing file: {str(e)}")
    except Exception as e:
        print(f"Error parsing file: {str(e)}")
    else:
        print(f"Successfully parsed file: {uploaded_file.name}")

    # Retrieve mapping rules based on relevant criteria
    mappings = Mapping.objects.filter(source=uploaded_file.name)  # Example using filename
    for mapping in mappings:
        try:
            parsed_data = df[mapping.field_name_source]  # Access data using Pandas
            transformed_data = transform_data(parsed_data, mapping.transformation_rule)
            # ... (store or use the transformed_data)
        except KeyError:
            print(f"Source field not found in DataFrame: {mapping.field_name_source}")

def transform_data(data, transformation_rule):
    """Implement your data transformation logic here based on the rule."""
    if transformation_rule == 'split_by_comma':
        return data.str.split(',')
    else:
        return data
