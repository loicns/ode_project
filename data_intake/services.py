from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest  # Import for error responses
from rest_framework import serializers  # For data validation
import pandas as pd
import spacy
import logging

def parse_and_preprocess(uploaded_file, request=None):
    """Parses and preprocesses uploaded data (structured or unstructured).

    Args:
        uploaded_file: The uploaded file object.
        request: Optional request object (needed for error responses in views).

    Returns:
        The preprocessed data.

    Raises:
        Exception: If an error occurs during parsing.
    """

    try:
        # Structured data (CSV, spreadsheet)
        if uploaded_file.name.endswith(('.csv', '.xlsx', '.xls')):
            data = pd.read_csv(uploaded_file)  # Adjust for Excel formats
            # ... (preprocessing logic using Pandas)

        # Unstructured data (text, OCR results)
        else:
            nlp = spacy.load('en_core_web_sm')  # Load spaCy model (adjust language as needed)
            data = nlp(uploaded_file.read().decode())
            # ... (preprocessing logic using spaCy)

        # Data validation (custom logic or Django-REST-Framework validators)
        # ... (validation code)

        return data

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error parsing file '{uploaded_file.name}': {str(e)}")

        # Handle error response (if request is provided)
        if request:
            if request.is_ajax():
                return JsonResponse({'error': str(e)}, status=400)
            else:
                return render(request, 'error_page.html', {'error_message': str(e)})
