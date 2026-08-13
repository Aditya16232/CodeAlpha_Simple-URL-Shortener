# Implementation: Simple URL Shortener

## Architecture

```
Browser (frontend)
   │  POST /shorten  {long_url}
   ▼
Flask App (app.py)
   │
   ├─ Generate unique short code
   ├─ INSERT INTO urls (short_code, long_url, created_at)
   └─ Return {short_code, short_url}
   │
Browser ── GET /<short_code> ──► Flask ── lookup DB ──► 302 Redirect to long_url
```

- **app.py** — Flask routes (shorten + redirect) and app bootstrap
- **database.py** — SQLite connection helpers and schema initialization
- **templates/** — Jinja2 HTML templates for the frontend
- **static/** — CSS/JS for the frontend
- **urls.db** — SQLite database file (created at runtime, gitignored)

## Database Schema (SQLite)

```sql
CREATE TABLE IF NOT EXISTS urls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code  TEXT UNIQUE NOT NULL,
    long_url    TEXT NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_short_code ON urls (short_code);
```

## API Design

### `POST /shorten`
Accept a long URL and return a short code.

- **Request body:** JSON `{"long_url": "https://..."}` (also supported from the form frontend)
- **Validation:** reject empty strings and non-http(s) URLs
- **Response (200):**
  ```json
  {
    "short_code": "aB3xYz",
    "short_url": "http://localhost:5000/aB3xYz",
    "long_url": "https://example.com/very/long/path"
  }
  ```

### `GET /<short_code>`
Resolve a short code and redirect.

- **Success:** HTTP `302 Found` with `Location: <long_url>`
- **Unknown code:** HTTP `404` → friendly "Link not found" page

### `GET /`
Serve the frontend landing page (form to shorten).

## Short Code Generation
- Use `secrets.choice()` over a base62 alphabet (`a–z`, `A–Z`, `0–9`) for crypto-secure randomness
- Default length: 6 characters (≈ 56 billion combinations — collision-safe)
- On the rare collision (`UNIQUE` constraint violation), regenerate the code and retry (max 5 attempts)

## Project Structure

```
url-shortener/
├── app.py              # Flask app: routes, logic
├── database.py         # DB init + helpers (init_db, insert_url, get_url)
├── requirements.txt    # flask
├── templates/
│   ├── index.html      # input form + result display
│   └── 404.html        # link-not-found page
├── static/
│   ├── style.css       # minimal styling
│   └── app.js          # fetch POST /shorten, show result, copy button
└── urls.db             # SQLite database (auto-created, gitignored)
```

## Frontend Flow
1. User enters a long URL in the input box.
2. JS `fetch()`es `POST /shorten` with `{long_url}`.
3. On success, the short link is displayed with a **Copy** button.
4. Clicking the short link opens the original URL (redirect handled by the backend).

## Running the Project

```bash
# 1. Create a virtual environment (first time only)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
python app.py                 # serves on http://localhost:5000
```

Open `http://localhost:5000` in a browser to use the frontend, or call the API directly:

```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d "{\"long_url\": \"https://example.com\"}"
```

## Test Plan
1. **Shorten:** POST a valid URL → expect a 6-char code and working short URL.
2. **Uniqueness:** Shorten two different URLs → codes differ.
3. **Redirect:** GET the short code → 302 to the original URL.
4. **Unknown code:** GET a random/nonexistent code → 404 page.
5. **Validation:** POST an empty/invalid URL → 400 error.
6. **Persistence:** Restart the server → previously shortened links still redirect.

## Future Enhancements (v2)
- Click counters / analytics
- Custom vanity slugs
- Link expiry
- Rate limiting and abuse protection
- Deploy behind a real domain (e.g., `s.example.com`)
