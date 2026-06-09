# Phase 5 — Django REST Framework (DRF)

**Goal:** Expose your data as a REST API — unlocks React/Vue frontends, mobile apps, AI pipelines, and third-party integrations.

---

## What You Will Learn

- What a REST API is and how it differs from a regular Django view
- How serializers convert models to JSON and validate incoming data
- How to build API views using `APIView` and generic views
- How to protect endpoints with token authentication
- How to add filtering, search, and pagination to your API

---

## 5.1 DRF Core Concepts

### Why REST APIs?

Regular Django views return HTML — only useful for browsers. A REST API returns JSON, which any client can consume: React frontends, mobile apps, AI pipelines, or third-party services.

| Django (HTML) | DRF (JSON) |
|---------------|------------|
| Template | Serializer |
| View | APIView / Generic View |
| Form | Serializer (also handles validation) |

### Serializers

| File | Purpose |
|------|---------|
| `blog/serializers.py` | Defines `PostSerializer` — converts `Post` instances to/from JSON |

`ModelSerializer` reads your model and generates fields automatically. `StringRelatedField` on a ForeignKey returns the string representation instead of a numeric ID.

Two jobs of a serializer:
- **Serialization** — Python model instance → JSON (for GET responses)
- **Deserialization** — incoming JSON → validated Python object (for POST/PUT requests)

### API Views

| File | Purpose |
|------|---------|
| `blog/views.py` | `PostListView` handles list + create, `PostDetailView` handles retrieve |
| `blog/urls.py` | Maps `/api/posts/` and `/api/posts/<pk>/` to the views |
| `core/urls.py` | All API routes live under `/api/` prefix |

`generics.ListCreateAPIView` combines GET (list) and POST (create) automatically — pagination, filtering, and permissions applied without writing `get()` and `post()` manually.

`perform_create()` is where you inject values before saving (e.g. setting `author` from the logged-in user).

---

## 5.2 Authentication in DRF

| File | Purpose |
|------|---------|
| `core/settings.py` | Configures `TokenAuthentication` and `IsAuthenticatedOrReadOnly` |
| `core/urls.py` | `/api/token/` endpoint returns a token for valid credentials |

**How token auth works:**
```
Client POSTs username + password to /api/token/
        ↓
DRF returns a token string
        ↓
Client sends "Authorization: Token <token>" header on every request
        ↓
DRF validates the token and identifies the user
```

`IsAuthenticatedOrReadOnly` — anyone can GET (read), only authenticated users can POST/PUT/DELETE (write).

`SessionAuthentication` is kept alongside token auth so the browsable API still works in the browser.

---

## 5.3 Filtering, Pagination & Throttling

All configured in `REST_FRAMEWORK` settings in `core/settings.py`.

| Feature | How it works |
|---------|-------------|
| **Filtering** | `?published=true` filters by field value via `DjangoFilterBackend` |
| **Search** | `?search=keyword` searches across `title` and `content` via `SearchFilter` |
| **Pagination** | `?page=2` returns the next page — response includes `count`, `next`, `previous`, `results` |
| **Throttling** | Anonymous users: 10 requests/min. Authenticated users: 30 requests/min |

Pagination only works automatically with generic views (`ListCreateAPIView`) — with raw `APIView` you must call the paginator manually.

---

## API Endpoints

| Method | URL | Auth required | Description |
|--------|-----|---------------|-------------|
| GET | `/api/posts/` | No | List all posts (paginated) |
| POST | `/api/posts/` | Yes | Create a new post |
| GET | `/api/posts/<pk>/` | No | Retrieve a single post |
| POST | `/api/token/` | No | Get an auth token |

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

Get a token:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

---

## Checkpoint

You should now understand:
- How serializers replace templates in an API context
- The difference between `APIView` (manual, explicit) and generic views (automatic, concise)
- How token authentication protects write endpoints
- How filtering, search, and pagination are configured globally via `REST_FRAMEWORK` settings

Move to [Phase 6](../phase-06-testing-quality/) when ready.
