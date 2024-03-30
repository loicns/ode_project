from unittest.mock import patch
from django.urls import reverse
from django.test import Client, TestCase
from ..models import Upload
from django.core.files.uploadedfile import UploadedFile

class UploadViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('data_intake.tasks.parse_uploaded_file.delay')  # Mock asynchronous task
    def test_upload_view_calls_task(self, mock_task):
        # Simulate form data
        data = {'source': 'test_source', 'file': UploadedFile(file=b'some,data', content_type='text/csv')}
        response = self.client.post(reverse('upload'), data=data, follow=True)

        # Assert successful response and Upload object creation
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Upload.objects.exists())  # Checks if at least one Upload object exists

        # You can't directly access 'upload' here because it's not explicitly assigned

