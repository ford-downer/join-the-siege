import unittest
import os
from pathlib import Path
import sys
import io

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from src.app import app

class TestDocumentAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create test files
        self.test_files_dir = os.path.join(project_root, "files")
        self.test_files = {
            'invoice': os.path.join(self.test_files_dir, "invoice_1.pdf"),
            'bank_statement': os.path.join(self.test_files_dir, "bank_statement_1.pdf"),
            'drivers_license': os.path.join(self.test_files_dir, "drivers_license_2.pdf")
        }

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_classify_invoice(self):
        """Test invoice classification endpoint."""
        with open(self.test_files['invoice'], 'rb') as f:
            data = {'file': (io.BytesIO(f.read()), 'invoice.pdf')}
            response = self.app.post('/classify_file', 
                                   content_type='multipart/form-data',
                                   data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['file_class'], 'invoice')
            self.assertGreater(response.json['confidence'], 0.7)

    def test_classify_bank_statement(self):
        """Test bank statement classification endpoint."""
        with open(self.test_files['bank_statement'], 'rb') as f:
            data = {'file': (io.BytesIO(f.read()), 'bank_statement.pdf')}
            response = self.app.post('/classify_file',
                                   content_type='multipart/form-data',
                                   data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['file_class'], 'bank_statement')
            self.assertGreater(response.json['confidence'], 0.65)

    def test_classify_drivers_license(self):
        """Test driver's license classification endpoint."""
        with open(self.test_files['drivers_license'], 'rb') as f:
            data = {'file': (io.BytesIO(f.read()), 'drivers_license.pdf')}
            response = self.app.post('/classify_file',
                                   content_type='multipart/form-data',
                                   data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['file_class'], 'drivers_license')
            self.assertGreater(response.json['confidence'], 0.6)

    def test_missing_file(self):
        """Test error handling when no file is provided."""
        response = self.app.post('/classify_file')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_invalid_file_type(self):
        """Test error handling for invalid file type."""
        data = {'file': (io.BytesIO(b'invalid file content'), 'test.txt')}
        response = self.app.post('/classify_file',
                               content_type='multipart/form-data',
                               data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main() 