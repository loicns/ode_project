from unittest import TestCase
from ..models import Upload
from django.test import TestCase
from ..models import Upload

class UploadModelTest(TestCase):

    def test_upload_creation(self):
        upload = Upload.objects.create(source='form', filename='test.csv')
        self.assertEqual(upload.source, 'form')
        self.assertEqual(upload.filename, 'test.csv')
        # You can add more assertions for other model fields/behavior