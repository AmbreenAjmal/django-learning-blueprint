# Phase 1 — Getting Started with Django

**Goal:** Get Django running locally, understand the project structure, and push your first Django app to GitHub.

---

## What You Will Learn

- How to set up a Django project from scratch
- What every generated file does and why it exists
- How Django's request lifecycle works
- How to create a view, wire up a URL, and render a template

---

## 1.1 Installation

- Python 3.10+, pip, and git are required
- Create a virtual environment and activate it
- Install Django with pip
- Verify with `django-admin --version`

---

## 1.2 Project & App Structure

Run `django-admin startproject core .` to scaffold the project, then `python manage.py startapp pages` to create your first app.

**Key files and what they do:**

| File | Purpose |
|------|---------|
| `manage.py` | Your main CLI tool — you use this to run the server, apply migrations, create apps, and more. You never edit this file. |
| `core/settings.py` | All project configuration: installed apps, database, templates, static files |
| `core/urls.py` | Root URL dispatcher — decides which app handles which URL |
| `pages/views.py` | Contains view functions — each one receives a request and returns a response |
| `pages/urls.py` | App-level URL patterns that map URLs to specific view functions |
| `pages/templates/pages/home.html` | The HTML template rendered by the view |

---

## 1.3 The Django Request Lifecycle

```
Browser sends request
        ↓
core/urls.py       → matches the URL, delegates to the right app
        ↓
pages/urls.py      → maps the URL to a specific view function
        ↓
pages/views.py     → runs the logic and calls render()
        ↓
home.html          → template is filled and returned as HTML
        ↓
Response sent back to the browser
```

Read the files in this order to trace a request end to end:
`core/urls.py` → `pages/urls.py` → `pages/views.py` → `pages/templates/pages/home.html`

---

## 1.4 Running the Project

```bash
python3 -m venv venv
source venv/bin/activate
pip install django
python manage.py runserver
```

Open `http://127.0.0.1:8000` to see the running app.

---

## Checkpoint

You should now understand:
- The difference between a Django **project** (`core/`) and an **app** (`pages/`)
- What each file is responsible for
- How a request travels from the browser through urls → view → template and back

Move to [Phase 2](../phase-02-mvt-blog/) when ready.
