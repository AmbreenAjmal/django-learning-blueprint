# Django Learning Blueprint

A hands-on, phase-by-phase guide to learning Django — from zero to a production-ready full-stack project. Every phase lives in its own folder with a working Django project and a README you can follow step by step.

> **Who is this for?**  Anyone who knows basic Python and wants to build real web apps with Django.

---

## Prerequisites

Before starting, you should be comfortable with:

- Variables, data types, loops, and functions
- Lists and dictionaries
- Basic file handling and error handling
- `git add` / `git commit` / `git push` — even just the basics

If any of these feel shaky, spend a week on Python fundamentals first. Django will make much more sense.

---

## Roadmap at a Glance

| Phase | Folder | Goal |
|-------|--------|------|
| 1 | [phase-01-getting-started](./phase-01-getting-started/) | Install Django, understand project structure, push your first app |
| 2 | [phase-02-mvt-blog](./phase-02-mvt-blog/) | Master Models, Views, Templates — build a blog from scratch |
| 3 | [phase-03-builtin-features](./phase-03-builtin-features/) | Admin, authentication, forms, static & media files |
| 4 | [phase-04-advanced-patterns](./phase-04-advanced-patterns/) | Managers, signals, middleware, caching, email |
| 5 | [phase-05-rest-api-drf](./phase-05-rest-api-drf/) | Build a REST API with Django REST Framework |
| 6 | [phase-06-testing-quality](./phase-06-testing-quality/) | Tests, code quality tools, security checklist |
| 7 | [phase-07-capstone](./phase-07-capstone/) | One complete production-quality project |
| — | [quick-reference](./quick-reference/) | Commands, packages, and resources cheat sheet |

Work through the phases **in order**. Each phase ends with a checkpoint project you commit and push.

---

## How to Use This Repo

1. **Clone the repo**
   ```bash
   git clone https://github.com/AmbreenAjmal/django-learning-blueprint.git
   cd django-learning-blueprint
   ```

2. **Enter a phase folder**
   ```bash
   cd phase-01-getting-started
   ```

3. **Read the phase README** — it explains what you will build and why.

4. **Follow the steps**, build the project, and make sure it runs.

5. **Commit your checkpoint** before moving to the next phase.

---

## The Django Request Lifecycle

Understanding this flow makes every Django concept click:

```
Browser sends request
        ↓
    urls.py matches the URL
        ↓
    View function runs
        ↓
    Template renders
        ↓
    Response sent back to browser
```

Keep this mental model in mind throughout all phases.

---

