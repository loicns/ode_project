from unittest.mock import patch
from django.test import TestCase
from ..tasks import parse_uploaded_file

class TaskTest(TestCase):

    @patch('pandas.read_csv')  # Mock external library
    def test_parse_csv_file(self, mock_read_csv):
        # Simulate task arguments
        upload_id = 1
        uploaded_file = uploaded_file(file=b'some,csv,data', content_type='text/csv')

        parse_uploaded_file(upload_id, uploaded_file)

        mock_read_csv.assert_called_once_with(uploaded_file)  # Assert CSV parsing