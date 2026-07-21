# Authentication and Roles

Security and access control are foundational to any backend system. The Result Management System uses a **Session-Based Authentication** model and implements **Role-Based Access Control (RBAC)**.

## How Session Authentication Works Currently

If you examine [`app/routes/auth/login.py`](file:///home/srestho/.gemini/antigravity/worktrees/result-manager/backend-learning-path-docs/app/routes/auth/login.py), you will see the login logic:

1. The user submits a `LoginForm` (username and password).
2. The backend checks the credentials against the database models (`PrincipalDataInfo` or `TeacherAddInfo`).
3. If valid, the backend uses Flask's `session` object to store data securely in an encrypted browser cookie.
```python
# Example from login.py
if teacher:
    session.clear()
    session["teacher"] = True
    session["teacher_id"] = teacher.teacher_id
```
4. Subsequent requests from the browser include this cookie, allowing the server to identify the user and their role.

> [!WARNING]
> **Hardcoded Admin Credentials:**
> Notice in `login.py` that the admin credentials (`admin`/`admin123`) are hardcoded. In a production AI application, credentials should NEVER be hardcoded. They should be stored as hashed strings in the database or managed via secure environment variables.

## Role-Based Access Control (RBAC)

The system supports four distinct roles, each with different privileges and dashboard access:

1. **Admin**: The superuser. Can create new Principals.
2. **Principal**: Manages an entire institute. Can create Teachers, Departments, and Subjects, and assign Teachers to Subjects.
3. **Teacher**: Manages daily academic activities. Can add Students, mark Attendance, and enter Marks.
4. **Student**: (Implicit) While there doesn't seem to be a direct student login in the snippet, students are the entities being managed and graded.

Routes protect themselves by checking the session dictionary (e.g., verifying if `"teacher" in session`).

## Why this must evolve for AI

The current session-based authentication relies heavily on **Browser Cookies**.

> [!IMPORTANT]
> **The AI Authentication Challenge:**
> If you build an autonomous AI Agent that needs to act on behalf of a Teacher (e.g., to fetch marks and write a summary report), the Agent doesn't have a web browser to store cookies.
>
> **The Solution (Phase 2):**
> We must migrate from stateful session cookies to **Stateless Tokens** (like JWT - JSON Web Tokens) or **API Keys**.
> When the AI Agent makes a request to the backend, it will include an `Authorization: Bearer <TOKEN>` header. The backend verifies the token and grants access without needing a browser session.
