# hticket — Invite-Only Ticketing Service

**Version:** 1.0  
**Status:** Approved for Development  
**Methodology:** Scrum

**Target Audience:** Backend & Frontend Developers

---

**Executive Summary**
- **What:** `hticket` (Project Nexus) is an invite-only project management and ticketing platform. Users may join only via manager-generated email invitations — no public signup.
- **Frontend constraint:** Django templates are used for rendering, but *all* CRUD operations must happen inside modal popups (no full-page reloads). HTMX is used to fetch partials and handle AJAX interactions.

---

**Technology Stack**
- **Backend:** Python 3.11+, Django 5+
- **Database:** PostgreSQL (production), SQLite (development)
- **Frontend rendering:** Django templates
- **Frontend interactivity:** HTMX (required). Optional: Hyperscript or Alpine.js for light UI logic.
- **CSS:** Bootstrap 5 (recommended) or Tailwind CSS
- **Async tasks / email:** Celery + Redis

---

**Data Models (high level)**
- **Custom User (`accounts.User`)**: extends `AbstractUser`.
    - `id` (UUID, PK)
    - `email` (unique, USERNAME_FIELD)
    - `role` (choices: `MANAGER`, `MEMBER`)
    - `avatar` (optional)
- **Invitation (`invitations.Invitation`)**: invite tokens and lifecycle.
    - `token` (UUID, unique)
    - `email` (indexed)
    - `sender` (FK -> User)
    - `project` (FK -> Project, nullable — auto-add on join)
    - `is_used` (bool)
    - `expires_at` (datetime)
- **Project (`projects.Project`)**
    - `name`, `description`
    - `members` (M2M -> User)
    - `created_by` (FK -> User)
- **Ticket (`tickets.Ticket`)**
    - `project` (FK)
    - `reporter` (FK -> User)
    - `title`, `description` (supports Markdown)
    - `status` (OPEN, IN_PROGRESS, REVIEW, DONE)
    - `priority` (LOW, MEDIUM, HIGH, CRITICAL)
    - `created_at`

---

**Frontend: HTMX Modal Pattern (required)**

Implement this pattern for all modal CRUD interactions.

- **Base template**: keep a single modal container in `base.html` where HTMX injects partials. Example structure:

```html
<!-- include htmx -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<main>
    {% block content %}{% endblock %}
<main>

<!-- Modal container HTMX targets -->
<div id="modal" class="modal fade" tabindex="-1" aria-hidden="true">
    <div id="dialog" class="modal-dialog" hx-target="this"></div>
</div>
```

- **Trigger buttons**: use `hx-get` to fetch the form partial and Bootstrap attributes to open the modal. Example:

```html
<button hx-get="{% url 'ticket_create' project.id %}"
                hx-target="#dialog"
                data-bs-toggle="modal"
                data-bs-target="#modal">
    Create Ticket
</button>
```

- **View behavior**: views should return only partial templates when requested by HTMX. On successful POST, return `HTTP 204 No Content` with `HX-Trigger` headers to notify the client to refresh lists. Example:

```python
def ticket_create(request, project_id):
        if request.method == 'POST':
                form = TicketForm(request.POST)
                if form.is_valid():
                        ticket = form.save()
                        return HttpResponse(status=204, headers={'HX-Trigger': 'ticketListUpdated'})
        else:
                form = TicketForm()

        return render(request, 'tickets/partials/ticket_form.html', {'form': form})
```

On validation errors, re-render the form partial so the modal shows errors without a full page reload.

---

**Key Use Cases / Acceptance Criteria**

- **Invitations** (Manager): Manager opens Invite modal → enters email → system creates `Invitation` with UUID and emails the link. Invitation must be unique and expire.
- **Join via token** (Guest): Guest visits `/join/<uuid>/` → email pre-filled, read-only; creates user, sets `is_used=True`, logs user in.
- **Project isolation**: Dashboard shows only `Project` instances where `request.user` is a member. Use `Project.objects.filter(members=request.user)`.
- **Ticket CRUD**: All create/edit/delete operations happen in HTMX-driven modals; successes emit an `HX-Trigger` (e.g., `ticketListUpdated`) so lists/cards update.

---

**Security & Permissions**

- **Authentication:** All views require login except the join-by-token view.
- **Project membership check:** enforce that `request.user` is a project member (or manager) before allowing ticket create/update. Example check:

```python
if request.user not in project.members.all() and request.user.role != 'MANAGER':
        raise PermissionDenied
```

- **CSRF:** Ensure HTMX requests include CSRF. You can set `hx-headers` globally or configure via JS to attach the CSRF token to HTMX requests.

---

**Development Setup (quick)**

Prerequisites: Python 3.11+, Redis for Celery (dev can use `EMAIL_BACKEND` console), PostgreSQL for production.

Typical setup commands:

```bash
git clone <repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # or: pip install django psycopg2-binary django-htmx django-crispy-forms celery redis
```

Environment variables (.env) examples:

```
DEBUG=True
SECRET_KEY=change_me
DB_NAME=nexus_db
DB_USER=postgres
DB_PASSWORD=postgres
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Important: set `AUTH_USER_MODEL = 'accounts.User'` in `settings.py` before running migrations for the first time.

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the dev server:

```bash
python manage.py runserver
```

---

**Notes for Developers**

- Follow the HTMX modal pattern strictly for all CRUD interactions: trigger → partial → POST → 204 + HX-Trigger.
- Keep modal partials small and focused (single form / single resource).
- Use Celery for background email sends (in production); the console backend is fine for local development.

---

If you'd like, I can also:
- add a `requirements.txt` or `pyproject.toml`,
- scaffold the `accounts`, `invitations`, `projects`, and `tickets` apps with basic models and admin, or
- add HTMX CSRF helper JS and a modal partial example.

Tell me which of the above you'd like next.
