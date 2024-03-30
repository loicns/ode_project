from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import Mapping
from .forms import MappingForm  # Import the form
from django.core.exceptions import ValidationError  # For raising validation errors

def mapping_view(request):
    if request.method == 'POST':
        form = MappingForm(request.POST)
        if form.is_valid():
            try:
                # Save or update Mapping object based on user input
                mapping = form.save()
                messages.success(request, 'Mapping configuration saved successfully!')
                return redirect('mapping_list')  # Redirect to mapping list view
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                # Consider logging the error for further debugging
        else:
            # Display specific error messages for each field with errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field '{field}': {error}")
            messages.error(request, 'Please correct the highlighted fields.')  # Generic error message

    # ... (rest of the view logic)

    else:
        # Prepare form or context data for GET requests
        form = MappingForm()  # Create an empty form instance for GET requests

    context = {'form': form}
    return render(request, 'data_mapping/mapping_form.html', context)  # Render template with form

def mapping_list(request):
    mappings = Mapping.objects.all()  # Fetch all Mapping objects
    context = {'mappings': mappings}
    return render(request, 'data_mapping/mapping_list.html', context)

def process_data(request):
  if request.method == 'POST':
    try:
      data = request.POST.dict()  # Access form data as a dictionary
    except Exception as e:
      return HttpResponseBadRequest(f"Error accessing request data: {str(e)}")

    # Sample validation logic (replace with your specific requirements)
    errors = {}  # Create a dictionary to store validation errors
    if not data.get('name'):
      errors['name'] = 'Name is required.'
    if not data.get('email') or '@' not in data.get('email'):
      errors['email'] = 'Please enter a valid email address.'
    if data.get('age') and not data.get('age').isdigit():
      errors['age'] = 'Age must be a number.'

    # Raise a ValidationError if there are errors
    if errors:
      raise ValidationError(errors)  # Raise a validation error with the error dictionary

    # Process the data (assuming validation is successful)
    cleaned_data = data.copy()  # Create a copy of validated data

    # Access and process specific data fields
    name = cleaned_data.get('name')
    email = cleaned_data.get('email')
    age = int(cleaned_data.get('age')) if cleaned_data.get('age') else None  # Handle optional age
    # Handle successful processing
    messages.success(request, 'Data processed successfully!')
    return redirect('some_view_name')  # Redirect to a suitable view

  else:
    # Handle GET requests (optional)
    # ...

   return HttpResponseBadRequest("Unsupported request method")  # Handle invalid requests