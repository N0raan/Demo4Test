import unittest
import sqlite3
import os.path
import time
from app import app

class ContactAPITestCase(unittest.TestCase):
    def setUp(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'Test.db')
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['DATABASE'] = db_path
        with app.app_context():
            conn = sqlite3.connect(db_path)
            conn.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, subject TEXT NOT NULL, webURL TEXT NOT NULL, text TEXT NOT NULL)')
            conn.commit()
            conn.close()

    def test_add_contact(self):
        response = self.app.post('/contact', json={'name': 'John Doe', 'email': 'john@example.com', 'subject': 'Test Subject', 'webURL': 'http://example.com', 'text': 'This is a test message'})
        self.assertEqual(response.status_code, 201)

    def test_get_contact(self):
        # Add a contact first to test retrieval
        self.app.post('/contact', json={'name': 'Jane Smith', 'email': 'jane@example.com', 'subject': 'Another Subject', 'webURL': 'http://example.com', 'text': 'Another test message'})
        # Now, try to retrieve the contact
        response = self.app.get('/contact/1')
        self.assertEqual(response.status_code, 200)
        # Additional assertions to check the content of the response

    def test_update_nonexistent_contact(self):
        response = self.app.put('/contact/999', json={'name': 'Updated Contact', 'email': 'updated@example.com', 'subject': 'Updated Subject', 'webURL': 'http://example.com', 'text': 'Updated message'})
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_contact(self):
        response = self.app.delete('/contact/999')
        self.assertEqual(response.status_code, 404)

    def test_response_time(self):
        start_time = time.time()
        response = self.app.get('/contact')
        end_time = time.time()

        # Replace 'your-expected-time' with the threshold response time you expect
        self.assertTrue(end_time - start_time < 0.5, "The response time exceeded the expected threshold.")    

if __name__ == '__main__':
    unittest.main()
