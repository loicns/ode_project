from unittest.mock import patch
from django.test import TestCase
from .tasks import parse_uploaded_file  # Assuming tasks are in the same directory as the test file
from django.core.files.uploadedfile import SimpleUploadedFile

class TaskTest(TestCase):

    @patch('pandas.read_csv')  # Patch pandas globally
    def test_parse_csv_file(self, mock_read_csv):
        # Simulate task arguments
        upload_id = 1
        uploaded_file = SimpleUploadedFile(
            name='test.csv', content=b'some,csv,data', content_type='text/csv'
        )

        # Call the task directly
        parse_uploaded_file(upload_id, uploaded_file)

        # Assert that pandas.read_csv was called with the correct argument
        mock_read_csv.assert_called_once_with(uploaded_file)
