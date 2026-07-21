# Current Architecture

Before we can modernize this application for AI, we need to understand how it is currently built. The Result Management System is a classic monolithic web application built using the Flask framework in Python.

## The Application Factory Pattern

If you look at [`run.py`](file:///home/srestho/.gemini/antigravity/worktrees/result-manager/backend-learning-path-docs/run.py) and [`app/__init__.py`](file:///home/srestho/.gemini/antigravity/worktrees/result-manager/backend-learning-path-docs/app/__init__.py), you will see the **Application Factory Pattern**.

Instead of creating the Flask app instance globally, the app is created inside a function `create_app()`.
```python
# From app/__init__.py
def create_app(): 
    app = Flask(__name__) 
    app.config.from_object(Config)
    db.init_app(app) 
    
    # ... blueprint registrations ...
    return app
```

> [!NOTE]
> **Why this matters for AI:** When you start adding Celery workers for asynchronous AI tasks (like processing a large document), having an application factory makes it much easier to initialize the background workers with the same configuration and database connections as your web app.

## Modular Routing with Blueprints

The `app/routes/` directory contains all the endpoints, organized by role: Admin, Auth, Principal, Teacher, Student.
Flask uses **Blueprints** to organize these routes. Instead of having hundreds of routes in one file, they are modularized.

For example, all routes related to the teacher's dashboard are grouped in a `teacher_dashboard_bp` Blueprint.

## The MVC (Model-View-Controller) Flow

Currently, the app follows a variation of the MVC pattern:
1. **Model:** The database layer (`app/models/`) managed by SQLAlchemy.
2. **View:** The HTML templates (`app/templates/`) rendered using Jinja2.
3. **Controller:** The route functions in (`app/routes/`) which handle the logic.

### A Typical Request Flow
1. A user navigates to `/login`.
2. The route function in `app/routes/auth/login.py` receives the request.
3. It checks the database via SQLAlchemy (`app/models/`) to verify credentials.
4. If successful, it sets a session cookie and redirects the user.
5. If the user requests a dashboard, the route function fetches data, passes it to a `.html` template in `app/templates/`, and returns the fully rendered HTML to the browser.

> [!WARNING]
> **The limitation for AI:** Returning fully rendered HTML is great for web browsers, but terrible for AI agents or mobile apps. An AI agent needs structured data (like JSON) to process, not HTML tags. In Phase 2, we will discuss how to break this MVC pattern to create APIs.

## Dependency Management

The project uses `requirements.txt` to manage dependencies. Key libraries include:
- `Flask`: The core web framework.
- `Flask-SQLAlchemy` & `SQLAlchemy`: ORM for database management.
- `Flask-WTF` & `WTForms`: For handling HTML form validation and rendering.
- `Jinja2`: The templating engine for generating HTML.
- `gunicorn`: A production-ready WSGI HTTP server used for deploying the application.
