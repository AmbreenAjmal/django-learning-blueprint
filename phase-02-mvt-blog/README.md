# Phase 2 — MVT Blog

**Goal:** Master Django's core pattern — Models, Views, Templates — by building a working blog from scratch.

---

## What You Will Learn

- How to define a database model and let Django manage the table for you
- How to query the database using the ORM (`Post.objects.all()`, `get_object_or_404`)
- How to build both a list view and a detail view
- How to link pages together using named URLs and template tags/filters

---

## 2.1 Models & the ORM

A **Model** is a Python class that maps to a database table — one class, one table; one instance, one row.

| File | Purpose |
|------|---------|
| `blog/models.py` | Defines the `Post` model — title, content, and an auto-set creation timestamp |
| `blog/migrations/` | Auto-generated history of changes to your models |
| `blog/admin.py` | Registers `Post` so you can manage posts from the admin panel |

Workflow whenever you change a model:
1. `python manage.py makemigrations` — Django detects the change and writes a migration file
2. `python manage.py migrate` — applies that migration to the actual database

---

## 2.2 Views

| File | Purpose |
|------|---------|
| `blog/views.py` | Contains `post_list` (fetches all posts) and `post_detail` (fetches one post by primary key) |

`post_list` uses `Post.objects.all()` — the ORM equivalent of `SELECT * FROM blog_post`.

`post_detail` uses `get_object_or_404(Post, pk=pk)` — fetches a single post or returns a clean 404 page if it doesn't exist.

Both pass data to a template via the **context dictionary**, the third argument to `render()`.

---

## 2.3 URL Configuration

| File | Purpose |
|------|---------|
| `blog/urls.py` | Maps `/` to `post_list` and `/post/<int:pk>/` to `post_detail` |
| `core/urls.py` | Delegates all root URLs to `blog.urls` via `include()` |

`<int:pk>` is a **URL converter** — it captures an integer from the path and passes it to the view as the `pk` argument.

---

## 2.4 Templates

| File | Purpose |
|------|---------|
| `blog/templates/blog/post_list.html` | Loops over all posts, shows a 15-word preview, links to the full post |
| `blog/templates/blog/post_detail.html` | Shows one post in full, with a link back to the list |

Key template features used:
- `{% for %}` / `{% endfor %}` — loop over the posts passed in context
- `{{ post.title }}` — variable output
- `{{ post.content|truncatewords:15 }}` — a **filter** that trims content to a preview
- `{{ post.created_at|date:"F j, Y" }}` — formats the timestamp
- `{% url 'post_detail' post.pk %}` — generates a URL from its name instead of hardcoding paths

---

## The Full Flow

```
Browser requests "/"
        ↓
core/urls.py        → delegates to blog.urls
        ↓
blog/urls.py        → matches "" to post_list
        ↓
blog/views.py       → post_list() queries Post.objects.all()
        ↓
post_list.html      → loops through posts, renders previews + links
        ↓
User clicks "Read more →"
        ↓
blog/urls.py        → matches "post/<int:pk>/" to post_detail
        ↓
blog/views.py       → post_detail() fetches one post by pk
        ↓
post_detail.html    → renders the full post
```

Trace it yourself by reading: `core/urls.py` → `blog/urls.py` → `blog/views.py` → templates.

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

Visit `/admin` to add posts, then `/` to view the blog.

---

## Checkpoint

You should now understand:
- How to define a model and persist it to the database via migrations
- How the ORM replaces raw SQL (`objects.all()`, `get_object_or_404`)
- How list and detail views differ, and how they share data with templates
- How named URLs (`{% url %}`) keep templates free of hardcoded paths

Move to [Phase 3](../phase-03-builtin-features/) when ready.
