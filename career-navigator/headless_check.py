import requests

BASE = 'http://127.0.0.1:5000'

s = requests.Session()

print('Fetching CSRF token from /api/get-csrf-token')
r = s.get(BASE + '/api/get-csrf-token')
print('Status:', r.status_code)
try:
    data = r.json()
except Exception:
    data = {'raw_text': r.text}
print('Response JSON:', data)
print('Cookies set in session:', s.cookies.get_dict())

print('\n--- Attempt 1: POST /api/test-csrf WITHOUT X-CSRFToken header ---')
r2 = s.post(BASE + '/api/test-csrf')
print('Status:', r2.status_code)
try:
    print('Body:', r2.json())
except Exception:
    print('Body:', r2.text)

print('\n--- Attempt 2: POST /api/test-csrf WITH X-CSRFToken header (from /api/get-csrf-token) ---')
csrf = data.get('csrf_token') or s.cookies.get('csrf_token')
print('Using token:', csrf)
headers = {'X-CSRFToken': csrf}
r3 = s.post(BASE + '/api/test-csrf', headers=headers)
print('Status:', r3.status_code)
try:
    print('Body:', r3.json())
except Exception:
    print('Body:', r3.text)

print('\nDone')
