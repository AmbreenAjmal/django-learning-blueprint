# Phase 6 — Testing & Code Quality

**Goal:** Write automated tests that prove your code works, then enforce style rules so the codebase stays clean as it grows.

---

## What You Will Learn

- How Django's test framework works and why tests matter
- How to write unit tests for models using `TestCase`
- How to test REST API endpoints using DRF's `APITestCase`
- How to measure test coverage with `coverage`
- How `flake8` catches style and logic errors
- How `black` auto-formats your code consistently
- How to audit your project for security issues

---

## 6.1 Why Test?

When your codebase is small you can manually verify everything. As it grows, manual testing breaks down — one change silently breaks something else. Automated tests run in seconds and tell you exactly what broke and why.

**Three types of tests you'll write here:**

| Type | What it tests | Tool |
|------|--------------|------|
| Unit test | A single model method or manager | `TestCase` |
| Signal test | That a side effect (Profile creation) happened | `TestCase` |
| API test | Full HTTP request/response cycle | `APITestCase` |

---

## 6.2 Django's Test Framework

| File | Purpose |
|------|---------|
| `blog/tests.py` | All tests for the blog app — models, signals, and API |

Django's test runner (`manage.py test`) discovers any method starting with `test_` inside a class that inherits from `TestCase` or `APITestCase`.

**Key concepts:**

- `setUp()` — runs before each test method. Creates the objects each test needs. Every test starts with a clean database.
- `TestCase` — Django base class. Wraps every test in a database transaction that is rolled back after the test, so tests never affect each other.
- `APITestCase` + `APIClient` — DRF equivalents. `APIClient` lets you make HTTP requests (GET, POST, etc.) in Python without a running server.
- `assertEqual`, `assertTrue`, `assertFalse` — assertion methods. If the assertion fails, the test fails and you see exactly which line.

**Flow of a single test:**
```
setUp() creates user, token, post
        ↓
test method calls self.client.get('/api/posts/')
        ↓
Django routes the request through real URL conf → real view
        ↓
View queries the real test database
        ↓
assertEqual checks the response status code
        ↓
Database rolled back — next test starts clean
```

---

## 6.3 What the Tests Cover

| Test Class | Tests |
|------------|-------|
| `PostModelTest` | `__str__` output, PublishedManager filters unpublished, default manager returns all |
| `ProfileSignalTest` | Profile auto-created when user is created, not duplicated on user update |
| `PostAPITest` | Unauthenticated GET allowed, unauthenticated POST → 403, authenticated POST → 201, author injected from token (not body), filter by `published`, search by title, retrieve single post |

---

## 6.4 Coverage

| Tool | Purpose |
|------|---------|
| `coverage` | Tracks which lines were executed during tests |

Coverage tells you the percentage of your code that tests actually run. 100% coverage does not mean bug-free code — it means every line was executed at least once.

**Flow:**
```
coverage run → executes tests while tracking line hits
        ↓
coverage report → shows % per file in terminal
        ↓
coverage html → generates htmlcov/index.html with colour-coded source
```

---

## 6.5 Code Quality Tools

| File | Purpose |
|------|---------|
| `.flake8` | Configuration for flake8 — max line length, excluded paths |
| `pyproject.toml` | Configuration for black — line length, excluded paths |

**flake8** — a linter. It reads your code without running it and flags:
- Unused imports
- Undefined variables
- Lines that are too long
- Spacing and indentation violations

**black** — a formatter. It rewrites your code automatically to follow one consistent style. You never argue about formatting in code reviews — black decides.

The two tools complement each other: black formats, flake8 catches logic issues black can't fix.

---

## 6.6 Security Audit

Django ships a built-in security checker that compares your settings against a production checklist.

| Issue flagged | Meaning |
|--------------|---------|
| `DEBUG = True` | Must be `False` in production |
| `SECRET_KEY` not changed | Default key is publicly known — rotate it |
| `ALLOWED_HOSTS` empty | Must list your domain in production |
| No HTTPS settings | `SECURE_SSL_REDIRECT`, `HSTS` headers not configured |

The check command is safe — it reads settings and prints warnings, it changes nothing.

---

## Running the Project

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Running Tests

```bash
# Run all tests
python manage.py test

# Run a specific test class
python manage.py test blog.tests.PostAPITest

# Run a single test method
python manage.py test blog.tests.PostAPITest.test_create_post_with_token_returns_201
```

You should see output like:
```
......
----------------------------------------------------------------------
Ran 10 tests in 0.312s

OK
```

Each `.` is one passing test. An `F` means a failure and Django will print exactly which assertion failed.

---

## Measuring Coverage

```bash
# Run tests under coverage
coverage run manage.py test

# Print report in terminal
coverage report

# Generate HTML report (open htmlcov/index.html in browser)
coverage html
```

The HTML report highlights every line in green (executed) or red (not covered by any test).

---

## Running flake8

```bash
flake8 .
```

No output means no issues. Any output shows the file, line number, and the violation code (e.g. `E302 expected 2 blank lines`).

---

## Running black

```bash
# Check what black would change (safe — does not modify files)
black --check .

# Apply formatting
black .
```

---

## Security Check

```bash
python manage.py check --deploy
```

In development you will see warnings about `DEBUG=True` and missing HTTPS settings — expected. This command is for auditing what would need to change before a production deploy.

---

## Checkpoint

You should now understand:
- How `TestCase` and `APITestCase` isolate tests with clean databases
- Why `setUp()` exists and what happens between tests
- How `APIClient` simulates real HTTP requests without a running server
- How coverage reveals untested code paths
- The difference between flake8 (linting) and black (formatting)
- What Django's security checklist flags and why

Move to [Phase 7](../phase-07-capstone/) when ready.
