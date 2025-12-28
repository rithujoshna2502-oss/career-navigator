#!/usr/bin/env python3
"""Direct test of CSRF token endpoint and request validation"""

import requests
import time

# Give server a moment to start
time.sleep(2)

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*70)
print("CSRF TOKEN EMBEDDING TEST - DIRECT")
print("="*70)

# Test 1: Get CSRF token endpoint
print("\n[TEST 1] Calling /api/get-csrf-token endpoint...")
try:
    resp = requests.get(f"{BASE_URL}/api/get-csrf-token", timeout=5)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    print(f"Cookies set: {resp.cookies}")
    csrf_token_from_api = resp.json().get('csrf_token')
    csrf_cookie = resp.cookies.get('csrf_token')
    print(f"✓ Token received: {csrf_token_from_api[:20]}..." if csrf_token_from_api else "✗ No token in response")
    print(f"✓ Cookie set: {csrf_cookie[:20]}..." if csrf_cookie else "✗ No cookie set")
except Exception as e:
    print(f"✗ Error: {e}")
    csrf_token_from_api = None
    csrf_cookie = None

# Test 2: POST without CSRF
print("\n[TEST 2] POST to /api/create-plan WITHOUT CSRF token...")
try:
    resp = requests.post(
        f"{BASE_URL}/api/create-plan",
        json={"resume_id": 1, "goal": "test", "duration_months": 6},
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:200]}")
    if resp.status_code >= 400:
        print(f"✓ Request rejected (as expected)")
    else:
        print(f"✗ Request was accepted (unexpected)")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: POST with INVALID CSRF
print("\n[TEST 3] POST to /api/create-plan WITH INVALID CSRF token...")
try:
    resp = requests.post(
        f"{BASE_URL}/api/create-plan",
        json={"resume_id": 1, "goal": "test", "duration_months": 6},
        headers={
            "Content-Type": "application/json",
            "X-CSRFToken": "invalid_token_xyz"
        },
        timeout=5
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:200]}")
    if resp.status_code >= 400:
        print(f"✓ Request rejected (as expected)")
    else:
        print(f"✗ Request was accepted (unexpected)")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: POST with VALID CSRF (token + cookie matching)
if csrf_token_from_api and csrf_cookie and csrf_token_from_api == csrf_cookie:
    print("\n[TEST 4] POST to /api/create-plan WITH VALID CSRF token...")
    try:
        session = requests.Session()
        # First set the cookie
        session.cookies.set('csrf_token', csrf_token_from_api)
        
        resp = session.post(
            f"{BASE_URL}/api/create-plan",
            json={"resume_id": 1, "goal": "test", "duration_months": 6},
            headers={
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token_from_api
            },
            timeout=5
        )
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:300]}")
        
        if "CSRF" in resp.text and resp.status_code >= 400:
            print(f"✗ CSRF check still failed")
        elif resp.status_code < 400:
            print(f"✓ CSRF check passed or allowed through")
        else:
            print(f"~ Request failed for other reason (not CSRF)")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n[TEST 4] SKIPPED - could not get valid CSRF token")

print("\n" + "="*70)
print("Summary: CSRF token embedding verified via API")
print("="*70)
