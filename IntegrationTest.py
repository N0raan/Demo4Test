import pytest
from app import app, db, Contact

@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def init_database():
    """Initialize a test database."""
    # Create the database and tables
    db.create_all()

    # Insert dummy data into the Contact table
    contact1 = Contact(name='John Doe', email='john@example.com', subject='Test Subject 1', webURL='http://example.com', text='Test message 1')
    contact2 = Contact(name='Jane Smith', email='jane@example.com', subject='Test Subject 2', webURL='http://example.com', text='Test message 2')

    # Add the contacts to the session and commit
    db.session.add(contact1)
    db.session.add(contact2)
    db.session.commit()

    yield  # Yield control to the test functions

    # Teardown - drop all tables
    db.drop_all()

def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Home Page" in response.data

def test_contact_page(client):
    """Test the contact page."""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b"Contact" in response.data

def test_create_contact(client):
    """Test creating a new contact."""
    response = client.post('/contact', data={
        'name': 'New Contact',
        'email': 'new@example.com',
        'subject': 'New Subject',
        'webURL': 'http://example.com',
        'text': 'New message'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thank you for contacting us!" in response.data

def test_contact_list(init_database, client):
    """Test retrieving the list of contacts."""
    response = client.get('/contacts')
    assert response.status_code == 200
    assert b"John Doe" in response.data
    assert b"Jane Smith" in response.data

if __name__ == '__main__':
    pytest.main()
