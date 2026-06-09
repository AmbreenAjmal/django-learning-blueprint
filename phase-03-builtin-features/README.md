# Phase 3 — Built-in Features

**Goal:** Unlock Django's powerful built-in tools — the admin panel, authentication system, forms, and static file handling.

---

## What You Will Learn

- How to customize the Django admin beyond its defaults
- How to add login/logout to your site using Django's built-in auth views
- How to protect views so only logged-in users can access them
- How to build a create form using ModelForms
- How to serve CSS and other static files properly

---

## 3.1 Django Admin

| File | Purpose |
|------|---------|
| `blog/admin.py` | Registers `Post` with a custom `ModelAdmin` class |

`list_display` controls which columns appear in the admin list view. `list_filter` adds a sidebar to filter records by field. `search_fields` adds a search box that queries specified fields.

The `@admin.register` decorator is a cleaner alternative to `admin.site.register()`.

---

## 3.2 Authentication

Django ships with a complete auth system — you only need to wire up the URLs and provide templates.

| File | Purpose |
|------|---------|
| `core/urls.py` | Includes `django.contrib.auth.urls` under `accounts/` |
| `core/settings.py` | Sets `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` |
| `blog/templates/registration/login.html` | The login form Django's built-in view looks for |

`django.contrib.auth.urls` provides ready-made URLs for login, logout, password change, and password reset — no view code needed.

In any template, `{{ user }}` and `user.is_authenticated` are available automatically — Django injects the current user into every template context via a context processor.

In Django 5.x, logout requires a **POST request** — use a `<form method="post">` instead of a plain link.

---

## 3.3 Forms & ModelForms

| File | Purpose |
|------|---------|
| `blog/forms.py` | Defines `PostForm` — a `ModelForm` for the `Post` model |
| `blog/views.py` | `post_create` view handles both GET (show form) and POST (validate & save) |
| `blog/templates/blog/post_form.html` | Renders the form with `{{ form.as_p }}` |

Key concepts:
- `ModelForm` generates form fields directly from the model — no manual field definition
- `commit=False` lets you modify the instance (e.g. set `author`) before saving
- `@login_required` redirects unauthenticated users to the login page automatically
- `{% csrf_token %}` is required on every POST form — protects against CSRF attacks

---

## 3.4 Static Files

| File/Folder | Purpose |
|-------------|---------|
| `static/css/style.css` | Project-wide stylesheet |
| `core/settings.py` | `STATIC_URL` and `STATICFILES_DIRS` tell Django where to find static files |

In templates, `{% load static %}` must appear at the top before using the `{% static %}` tag. `{% static 'css/style.css' %}` generates the correct URL regardless of where the project is deployed.

---

## The Full Flow

```
User visits "/"
        ↓
core/urls.py        → delegates to blog.urls
        ↓
blog/views.py       → post_list() fetches all posts, passes to template
        ↓
post_list.html      → checks user.is_authenticated, shows nav accordingly

User clicks "New Post"
        ↓
blog/urls.py        → routes to post_create view
        ↓
blog/views.py       → @login_required checks auth, handles GET/POST
        ↓
GET  → renders empty PostForm
POST → validates form, sets author, saves, redirects to post_list
```

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

Visit `/admin` to manage posts, `/accounts/login/` to log in, `/` to view the blog.

---

## Checkpoint

You should now understand:
- How to customize the Django admin with `ModelAdmin`
- How Django's built-in auth system works and how to wire it up
- How `ModelForm` + `@login_required` work together for protected form views
- How static files are served and referenced in templates

Move to [Phase 4](../phase-04-advanced-patterns/) when ready.
