import json
import pytest

from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client


def test_register_login_logout(client):
    # Register
    rv = client.post('/register', json={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123'
    })
    assert rv.status_code == 201
    data = rv.get_json()
    assert data.get('success') is True

    # Login
    rv = client.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'testpass123'
    })
    # Login may return JSON 200 or a redirect (302) depending on response handling
    assert rv.status_code in (200, 302)
    if rv.status_code == 200:
        data = rv.get_json()
        assert data.get('success') is True

    # Access protected API
    rv = client.get('/api/user-info')
    assert rv.status_code == 200
    u = rv.get_json()
    assert u.get('success') is True

    # Logout
    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200
