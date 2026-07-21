# RAG and Agents Integration

This is the final phase of your AI Engineering learning path. Once your backend is an API (Phase 2), you can introduce Intelligence (RAG) and Autonomy (Agents).

We will use the **Result Management System** as the context. Imagine a feature where a Principal can ask: *"Which subjects have the lowest attendance across the science department, and what are the average marks for those subjects?"*

## 1. Vector Databases & Embeddings

Standard SQL databases (like SQLite or PostgreSQL) are great for exact matches (e.g., `SELECT * FROM students WHERE roll = 101`). They are terrible at semantic meaning.

To give your AI context, you must translate your database records into **Vector Embeddings** (long arrays of numbers that capture meaning).

### How to do this in this project:
1. **Choose a Vector DB:** Use an external service like Pinecone, or a local solution like Milvus or `pgvector` (if migrating to PostgreSQL).
2. **Data Pipeline:** Write a Python script that runs nightly (perhaps using Celery). It will:
   - Query SQLAlchemy for Student Profiles, Attendance aggregates, and Marks.
   - Format this into text chunks: *"Student John Doe in Science group has 85% attendance. In Midterms, he scored 45/100 in Physics."*
   - Pass this text to an Embedding Model (like OpenAI's `text-embedding-3-small`).
   - Store the resulting vector alongside the text chunk in the Vector DB.

## 2. Implementing RAG (Retrieval-Augmented Generation)

When the Principal asks their complex question, an LLM alone won't know the answer because it doesn't have your school's data in its training weights. We use RAG to give it the data.

### The RAG Pipeline Architecture:
1. **Receive Query:** Backend receives the Principal's query via API.
2. **Embed Query:** Convert the Principal's question into a vector using the same embedding model.
3. **Semantic Search:** Query the Vector DB to find the most mathematically similar context vectors (e.g., retrieving chunks about Science department attendance and marks).
4. **Prompt Engineering:** Construct a prompt for the LLM (like Gemini or GPT-4):
   ```text
   System: You are an academic advisor. Answer the user's question using ONLY the provided context.
   Context: [Insert retrieved chunks from Vector DB here]
   User Query: Which subjects have the lowest attendance...
   ```
5. **Generation:** The LLM reads the context and generates an accurate, plain-English summary.
6. **Return:** The backend returns the summary to the Principal's dashboard.

## 3. Building Agentic Workflows

RAG is passive (it answers questions). Agents are active (they take actions).
To make an Agent in this system, you use **Function Calling (Tool Use)**.

### The Agentic Architecture:
1. You provide the LLM with a list of tools it can use. In our project, these tools would just be standard Python functions or API endpoints you built in Phase 2.
   - `get_student_marks(student_id)`
   - `send_email_to_parent(student_id, message)`
   - `flag_student_for_review(student_id, reason)`

2. **The Prompt:** *"You are an autonomous academic monitor. Review the latest mid-term results. If any student has dropped below a passing grade across 3 or more subjects, flag them for review and draft an email to their parent."*

3. **The Execution Loop:**
   - The LLM decides it needs data. It outputs a structured JSON response requesting to call `get_student_marks()`.
   - Your backend intercepts this, executes the Python function using SQLAlchemy, and feeds the result back to the LLM.
   - The LLM analyzes the data. It decides it needs to take action, so it outputs a request to call `flag_student_for_review()` and `send_email_to_parent()`.
   - Your backend executes those actions.

> [!CAUTION]
> **Safety First:**
> Never give an AI Agent a tool that deletes data (e.g., `drop_student_record()`) without implementing a "Human-in-the-Loop" approval step first.
