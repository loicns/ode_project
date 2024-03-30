from unittest.mock import patch
from django.urls import reverse
from django.test import Client, TestCase
from .models import Upload
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('data_intake.tasks.parse_uploaded_file.delay')  # Assuming tasks are in a separate 'data_intake' app
    def test_upload_view_calls_task(self, mock_task):
        # Simulate form data
        data = {'source': 'test', 'file': SimpleUploadedFile(
            name='test.csv', content=b'some,csv,data', content_type='text/csv'
        )}
        response = self.client.post(reverse('upload'), data=data, follow=True)

        # Assert successful response and Upload object creation
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Upload.objects.exists())  # Check if an Upload object was created

        # Access the created Upload object for further assertions if needed
        upload = Upload.objects.get()
        # Add assertions based on expected Upload object properties
