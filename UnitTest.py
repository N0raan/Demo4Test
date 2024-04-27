import unittest
import sqlite3
from app import app, get_db_connection

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.app = app.test_client()

        with app.app_context():
            # Initialize the in-memory database
            db = get_db_connection()
            db.create_all()
            db.session.commit()

    def test_contact_form_submission(self):
        """Test submitting the contact form."""
        response = self.app.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'webURL': 'http://example.com',
            'text': 'Test message'
        })

        assert response.status_code == 302  # Redirect status code

        # Check if the contact entry is added to the database
        with app.app_context():
            db = get_db_connection()
            contact = db.query(contact).filter_by(email='test@example.com').first()
            self.assertIsNotNone(contact)
            self.assertEqual(contact.name, 'Test User')
            self.assertEqual(contact.subject, 'Test Subject')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
