import requests
import pytest

@pytest.mark.parametrize("url", [
    ("http://127.0.0.1:8080/contact"),
    # Add more endpoints if needed
])
def test_response_status_code_500(url):
    response = requests.get(url)
    assert response.status_code == 500

@pytest.mark.parametrize("url", [
    ("http://127.0.0.1:8080/contact"),
    # Add more endpoints if needed
])
def test_response_content_type_html(url):
    response = requests.get(url)
    content_type = response.headers.get("Content-Type", "")
    assert "text/html" in content_type

@pytest.mark.parametrize("url", [
    ("http://127.0.0.1:8080/contact"),
    # Add more endpoints if needed
])
def test_key_error_handling_in_response(url):
    response = requests.get(url)
    assert "KeyError: 'name'" in response.text
