from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
import os
from ..models import Document

class DocumentViewsetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/documents/'
        self.test_file = SimpleUploadedFile('test_document.pdf', b'test content', content_type='file/pdf')
        self.document = Document.objects.create(title="Initial Test Document", file=self.test_file)

    def tearDown(self):
        if os.path.exists('documents/test_document.pdf'):
            os.remove('documents/test_document.pdf')
        if os.path.exists('documents/new_test_document.pdf'):
            os.remove('documents/new_test_document.pdf')
        if os.path.exists('documents/updated_test_document.pdf'):
            os.remove('documents/updated_test_document.pdf')

    def test_create_document_successful(self):
        document_file = SimpleUploadedFile('new_test_document.pdf', b'new test content', content_type='file/pdf')
        document_data = {
            'title': 'Test Document',
            'file': document_file
        }

        response = self.client.post(self.url, document_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {
            'id': response.data['id'],
            'title': 'Test Document',
            'uploaded_at': response.data['uploaded_at'],
            'file': f'http://testserver/documents/{document_file.name}'
        }

        self.assertEqual(response.data, expected_data)

    def test_get_documents_successful(self):
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.document.title)
        self.assertEqual(response.data[0]['file'], f'http://testserver/documents/{self.test_file.name}')
        
    def test_update_document_successful(self):
        updated_file = SimpleUploadedFile('updated_test_document.pdf', b'updated test content', content_type='file/pdf')
        updated_data = {
            'title': 'Updated Test Document',
            'file': updated_file
        }

        response = self.client.put(f'{self.url}{self.document.id}/', updated_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': response.data['id'],
            'title': 'Updated Test Document',
            'uploaded_at': response.data['uploaded_at'],
            'file': f'http://testserver/documents/{updated_file.name}'
        }

        self.assertEqual(response.data, expected_data)

    def test_patch_document_successful(self):
        updated_data = {
            'title': 'Partial Test Document'
        }

        response = self.client.patch(f'{self.url}{self.document.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': response.data['id'],
            'title': 'Partial Test Document',
            'uploaded_at': response.data['uploaded_at'],
            'file': f'http://testserver/documents/{self.test_file.name}'
        }

        self.assertEqual(response.data, expected_data)

    def test_delete_document_successful(self):
        response = self.client.delete(f'{self.url}{self.document.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(pk=self.document.pk).exists())
