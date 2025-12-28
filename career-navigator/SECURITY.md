# Security & Authentication Summary

## Authentication Layers (Already Implemented)

### 1. **Login Required (`@login_required` decorator)**
All sensitive endpoints enforce login:
- `POST /api/upload-resume` — resume uploads
- `POST /api/create-plan` — plan creation
- `GET /api/plan/<id>` — view user plans
- `POST /api/update-progress/<id>` — track progress
- `GET /api/agent/suggestions` — agent recommendations
- `POST /api/agent/apply-update` — apply updates
- Plus 10+ other user-scoped endpoints

**Public endpoints (no login required):**
- `GET /` — redirects to login if not authenticated
- `POST /register` — registration
- `POST /login` — login
- `GET /logout` — logout
- `POST /api/test-csrf` — CSRF validation test

### 2. **CSRF Protection (Double-Submit Pattern)**
- All state-changing endpoints verify `X-CSRF-Token` header matches cookie
- `@csrf.exempt` only on public endpoints (register, login, webhooks, admin APIs)
- CSRF token rotated on each request for sensitive operations

### 3. **API Key Authentication (New)**
- `GET /api/admin/users` — requires `Authorization: Bearer <API_KEY>` or `X-API-Key: <key>`
- Verified using timing-attack-safe `hmac.compare_digest`
- Set `API_ADMIN_KEY` environment variable for production

### 4. **Webhook Signature Verification (New)**
- `POST /webhook/example` — validates HMAC-SHA256 signature in `X-Signature` header
- Requires `WEBHOOK_SECRET` environment variable
- Protects against unauthorized webhook calls

### 5. **Session Security**
- `SESSION_COOKIE_HTTPONLY=True` — prevents JavaScript access to session cookie
- `SESSION_COOKIE_SAMESITE=Lax` — prevents cross-site cookie sending
- `SESSION_COOKIE_SECURE=True` (in production) — HTTPS-only cookie transmission

## Security Headers (Already Implemented)

All responses include:
- **Content-Security-Policy (CSP):** Restricts inline scripts, external resources, and frames
- **X-Content-Type-Options: nosniff** — prevents MIME-sniffing attacks
- **X-Frame-Options: DENY** — prevents clickjacking
- **Referrer-Policy: no-referrer** — hides referrer information
- **Strict-Transport-Security (HSTS):** Enforces HTTPS in production

## Data Sanitization (Already Implemented)

### Resume Upload Sanitization
When uploading resumes, parsed fields are HTML-escaped before storage:
- `skills` array → sanitized individual strings
- `experience_level`, `current_role`, `education` → escaped HTML

### HTML Escaping
All user inputs are escaped via `html.escape()` in `security_utils.py`:
```python
sanitized_input = sanitize_text(user_input)
```

## Environment Variables (Secrets Management)

**Never commit `.env` to Git. Use `.gitignore` and set vars in production via:**
- Railway Dashboard → Variables tab
- Heroku → Config Vars
- Docker → ENV file (secrets mounted separately)

Required secrets:
```
SECRET_KEY=<random-32-char-string>
DATABASE_URL=<database-connection-string>
WEBHOOK_SECRET=<random-secret-for-webhooks>
API_ADMIN_KEY=<random-key-for-admin-endpoints>
MAIL_PASSWORD=<sendgrid-api-key>
SESSION_COOKIE_SECURE=True  # Production only
```

## Testing Security

### Manual Tests
1. Try accessing protected endpoints without login → Should redirect to `/login`
2. Try CSRF on `/api/create-plan` without token → Should return 400
3. Try API key endpoint without key → Should return 401
4. Try webhook without signature → Should return 401

### Automated Tests (See `project/tests/`)
```bash
# Run all tests
pytest project/tests/ -v

# Run security tests
pytest project/tests/test_agents.py -v
pytest project/tests/test_planner.py -v
```

## Known Limitations & Next Steps

- **SQLite in production:** Works for dev/small scale; migrate to PostgreSQL for >1000 concurrent users
- **Rate limiting:** Not yet implemented; recommend adding `flask-limiter` for prod
- **Input validation:** Basic checks present; consider `marshmallow` or Pydantic for stricter validation
- **Background jobs:** Simple threading used; upgrade to Celery + Redis for production
- **HTTPS enforcement:** Auto-on with Railway/Heroku; ensure `SESSION_COOKIE_SECURE=True` in prod

## Deployment Security Checklist

- [ ] Remove hardcoded secrets from code
- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Use strong `SECRET_KEY` (32+ random characters)
- [ ] Set unique `WEBHOOK_SECRET` and `API_ADMIN_KEY`
- [ ] Use HTTPS (automatic on Railway/Heroku)
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated (`pip install --upgrade -r requirements.txt`)
- [ ] Consider adding rate limiting for public endpoints
- [ ] Regular backups of SQLite DB or migrate to managed DB

## References

- Flask Security: https://flask.palletsprojects.com/security/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CSP Guide: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
