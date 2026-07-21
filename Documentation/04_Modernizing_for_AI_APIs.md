# Modernizing for AI: APIs and Asynchrony

To prepare the Result Management System for Artificial Intelligence integration, we must decouple the frontend from the backend and rethink how we handle slow tasks.

## 1. The API-First Approach

Currently, routes like `teacher_dashboard.py` fetch data from the DB and pass it directly to `render_template("teacher/dashboard.html", ...)` to build a webpage.

AI Agents, Mobile Apps, and Modern Frontends (React/Vue) don't want HTML. They want **JSON (JavaScript Object Notation)**.

### The Refactor (RESTful APIs)

We need to convert our routes into REST API endpoints.

**Current (Monolithic):**
```python
@app.route('/students')
def view_students():
    students = AddStudentInfo.query.all()
    # Returns a fully rendered HTML page
    return render_template('students_list.html', students=students)
```

**Modernized (API):**
```python
from flask import jsonify

@app.route('/api/v1/students', methods=['GET'])
def api_get_students():
    students = AddStudentInfo.query.all()
    # Returns raw data that an AI or React frontend can parse
    student_data = [
        {"id": s.student_id, "name": s.student_full_name, "roll": s.student_roll} 
        for s in students
    ]
    return jsonify({"status": "success", "data": student_data})
```

> [!TIP]
> **Learning Checkpoint:**
> To learn real Backend AI engineering, practice converting one of the existing routes (e.g., getting a student's marks) into a JSON API endpoint using `jsonify`. Use Postman or `curl` to test it.

## 2. Authentication with JWT or API Keys

As discussed in [03_Authentication_and_Roles.md](./03_Authentication_and_Roles.md), AI agents can't use browser cookies.

When modernizing, you should implement **JSON Web Tokens (JWT)**.
1. When a user (or agent) hits `/api/v1/login` with correct credentials, the server returns a signed JWT string.
2. For all future requests, the agent sends that token in the HTTP Header: `Authorization: Bearer <TOKEN>`.
3. The server validates the token mathematically without needing to look up a session in memory.

## 3. Asynchronous Tasks (Celery & Redis)

Standard web requests are expected to return in milliseconds. But AI is slow.
If a teacher requests: *"Generate a 5-page performance report for John Doe using an LLM,"* the LLM API call might take 10-30 seconds.

If you run this synchronously in a Flask route, the web server will block, and the user's browser will spin indefinitely (eventually timing out).

### The Solution: Task Queues
You must introduce a message broker (like Redis) and an asynchronous worker (like Celery).

1. **API Receives Request:** The user asks for an AI report.
2. **Queue Task:** The Flask route packages the request and pushes it to a Redis queue.
3. **Immediate Response:** Flask immediately responds to the user: `{"task_id": "12345", "status": "processing"}`.
4. **Background Work:** A separate Celery worker process picks up the task from Redis, spends 20 seconds talking to OpenAI/Gemini, and saves the result to the database.
5. **Polling/WebSockets:** The frontend polls the backend (`/api/v1/task/12345`) or uses WebSockets to find out when the report is ready.

> [!IMPORTANT]
> **The Golden Rule of AI Backends:**
> **Never** execute long-running AI inference directly inside an HTTP request handler. Always offload it to a background worker.
