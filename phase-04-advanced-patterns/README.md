# Phase 4 — Advanced Patterns

**Goal:** Go beyond the basics — learn the patterns that professional Django developers use every day.

---

## What You Will Learn

- How to define reusable query logic using custom model managers
- How signals let parts of your app react to events without being directly connected
- How middleware intercepts every request and response in the pipeline
- How caching prevents unnecessary database queries
- How to send emails from Django

---

## 4.1 Custom Model Managers & QuerySets

| File | Purpose |
|------|---------|
| `blog/models.py` | Defines `PublishedManager` alongside the default `objects` manager |
| `blog/views.py` | Uses `Post.published_posts.all()` instead of `Post.objects.all()` |

Django gives every model a default manager called `objects`. A custom manager is just a class that extends `models.Manager` and overrides `get_queryset()` to apply a permanent filter.

The result: filtering logic lives in one place. Every view that calls `Post.published_posts.all()` automatically gets only published posts — no repeated `.filter(published=True)` scattered across views.

---

## 4.2 Signals

| File | Purpose |
|------|---------|
| `blog/models.py` | Defines `Profile` model and the `create_profile` signal receiver |

Django's signal system is an event bus. `post_save` fires every time a model instance is saved. `@receiver(post_save, sender=User)` subscribes a function to that event for the `User` model specifically.

The `created` argument distinguishes a new record (`True`) from an update (`False`) — the `if created` check prevents duplicate profiles when a user updates their account.

**Flow:**
```
User.objects.create_user(...)
        ↓
Django saves user to database
        ↓
post_save signal fires
        ↓
create_profile() runs automatically
        ↓
Profile created — no view code involved
```

---

## 4.3 Middleware

| File | Purpose |
|------|---------|
| `blog/middleware.py` | Logs the method, path, and duration of every request |
| `core/settings.py` | Registers the middleware at the top of `MIDDLEWARE` |

Middleware wraps the entire request/response cycle. Code before `self.get_response(request)` runs before the view. Code after runs after the view. The order in `MIDDLEWARE` matters — each middleware wraps the one below it.

**Pipeline:**
```
Browser request → RequestTimeMiddleware → SecurityMiddleware → ... → View → ... → Browser response
```

---

## 4.4 Caching

| File | Purpose |
|------|---------|
| `blog/views.py` | `@cache_page(60)` caches the post list for 60 seconds |

`@cache_page(seconds)` stores the full rendered HTML of a view. The first request hits the database and stores the result. All subsequent requests within the cache window are served instantly from memory — no database query at all.

After the cache expires the next request refreshes it. In production you'd use Redis or Memcached as the cache backend instead of Django's default in-memory cache.

---

## 4.5 Email

| File | Purpose |
|------|---------|
| `core/settings.py` | Sets `EMAIL_BACKEND` to the console backend for development |
| `blog/views.py` | Calls `send_mail()` after a post is created |

`django.core.mail.backends.console.EmailBackend` prints emails to the terminal instead of sending them — safe for development. Switching to a real SMTP provider in production is a single settings change.

`send_mail()` takes subject, message, from_email, and recipient_list. Django handles all the MIME formatting.

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

Watch the terminal — every request is logged by the middleware and emails print there too.

---

## Checkpoint

You should now understand:
- How custom managers keep query logic DRY and out of views
- How signals decouple automatic behavior from the code that triggers it
- How middleware intercepts every request without touching any view
- How `@cache_page` reduces database load with one decorator
- How Django's email system works in development vs production

Move to [Phase 5](../phase-05-rest-api-drf/) when ready.
