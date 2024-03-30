from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from .models import Upload
from .tasks import parse_uploaded_file  # Import asynchronous parsing task
from .services import parse_and_preprocess  # Import parsing and preprocessing function
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class UploadView(View):
    def get(self, request):
        # Render the upload form when a GET request is made
        return render(request, 'data_intake/upload_form.html')
    
    def post(self, request):
        if request.method == 'POST':
            uploaded_file = request.FILES.get('file')
            if uploaded_file is None:
                return HttpResponseBadRequest('No file uploaded')

            try:
                preprocessed_data = parse_and_preprocess(uploaded_file)

                # Update or create an Upload instance with preprocessed_data
                upload = Upload.objects.create(
                    source=request.META['REMOTE_ADDR'],  # Or set source based on logic
                    filename=uploaded_file.name,
                    file=uploaded_file,
                    data=preprocessed_data  # Add preprocessed_data to the instance
                )
                parse_uploaded_file.delay(upload.id, uploaded_file)

                return redirect('success')  # Redirect to success page

            except Exception as e:
                # Handle upload/processing errors gracefully
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error uploading/processing file '{uploaded_file.name}': {str(e)}")

                # Return an appropriate error message to the user
                error_message = "An error occurred while processing your file. Please try again later."
                return render(request, 'data_intake/index.html', {'error_message': error_message})

        # Consistent indentation for clarity
        return render(request, 'data_intake/upload_form.html')  # Upload form (replace with your form template)


def success_view(request):
    return HttpResponse('File uploaded successfully! Parsing will begin shortly in the background.')


class EmailParseView(View):
    def post(self, request):
        if request.method == 'POST':
            uploaded_file = request.FILES.get('file')

            if uploaded_file is None:
                return HttpResponseBadRequest('No file uploaded')

            # Validate uploaded file type (optional)
            if not uploaded_file.name.endswith('.eml') and not uploaded_file.name.endswith('.msg'):
                return HttpResponseBadRequest('Unsupported file format. Please upload an email file (.eml or .msg).')

            try:
                # Open the uploaded email file for parsing
                with open(uploaded_file.name, 'rb') as f:
                    message = email.message_from_binary(f.read())

                # Extract data from various parts of the email
                body_content = self.get_body_content(message)
                attachments = self.get_attachments(message)
                sender_name, sender_email = self.get_sender_info(message)
                subject = message['Subject']
                received_date = message['Date']

                # Store parsed data in the Upload model
                upload = Upload.objects.create(
                    source=request.META['REMOTE_ADDR'],
                    filename=uploaded_file.name,
                    file=uploaded_file,
                    body_content=body_content,
                    attachments=attachments,
                    sender_name=sender_name,
                    sender_email=sender_email,
                    subject=subject,
                    received_date=received_date
                )

                # Optional: Handle attachments (e.g., save to a designated location)
                # ...

                # Trigger asynchronous parsing task
                parse_uploaded_file.delay(upload.id, uploaded_file)

                return redirect('success')  # Redirect to success page

            except Exception as e:
                # Handle parsing errors gracefully
                print(f"Error parsing email: {str(e)}")
                return HttpResponseBadRequest('Error parsing email. Please try again or contact support.')

        # Render the email upload form (optional)
        return render(request, 'data_intake/email_upload_form.html')  # Replace with your email upload form template

# Helper functions for email parsing
    def get_body_content(self, message):
        if message.is_multipart():
            # Handle multipart messages (text/html)
            for part in message.walk():
                if part.is_body():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        return part.get_payload(decode=True).decode()
                    elif content_type == 'text/html':
                        return part.get_payload(decode=True).decode()
        else:
            # Handle single part messages
            content_type = message.get_content_type()
            if content_type == 'text/plain':
                return message.get_payload(decode=True).decode()
            elif content_type == 'text/html':
                return message.get_payload(decode=True).decode()
        return None  # No body content found

    def get_attachments(self, message):
        attachments = []
        if message.is_multipart():
            for part in message.walk():
                if part.is_attachment():
                    filename = part.get_filename()
                    content_type = part.get_content_type()
                    with open(f'uploads/attachments/{filename}', 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    attachments.append({'filename': filename, 'content_type': content_type})
        return attachments

    def get_sender_info(self, message):
        from_field = message['From']
        sender_name, sender_email = email.utils.parseaddr(from_field)
        return sender_name, sender_email
    
def home_view(request):
  """
  A simple view to render the home page.
  """
  return render(request, 'data_intake/index.html')