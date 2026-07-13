```                    RESULT MANAGEMENT SYSTEM
                     Team Git Workflow

               ┌────────────────────────┐
               │        main            │
               │  (Stable Production)   │
               └──────────┬─────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌───────────────────┐              ┌───────────────────┐
│ Rakib             │              │ Apra              │
│ Backend Developer │              │ Frontend Developer│
└─────────┬─────────┘              └─────────┬─────────┘
          │                                  │
          │ git checkout -b                  │ git checkout -b
          │ backend_feature                  │ frontend_feature
          ▼                                  ▼
  ┌─────────────────┐                 ┌─────────────────┐
  │ Coding          │                 │ Coding          │
  └────────┬────────┘                 └────────┬────────┘
           │                                   │
           │ git add .                         │ git add .
           │ git commit                        │ git commit
           │ git push                          │ git push
           ▼                                   ▼
 ┌────────────────────┐             ┌────────────────────┐
 │ origin/backend_*   │             │ origin/frontend_*  │
 └──────────┬─────────┘             └──────────┬─────────┘
            │                                  │
            └──────────────┬───────────────────┘
                           ▼
                 GitHub Pull Request
                           │
                     Code Review
                           │
                    Merge into main
                           │
                           ▼
                 ┌──────────────────┐
                 │ origin/main      │
                 └────────┬─────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
 git checkout main                git checkout main
 git pull origin main             git pull origin main
          │                               │
          ▼                               ▼
     New Feature                    New Feature
```

## Importance
প্রতিদিনের Workflow
### 1. কাজ শুরু করার আগে (দুজনই)
```bash
git checkout main
git pull origin main
```
### 2. নতুন Feature Branch
- Rakib
```bash
git checkout -b backend_marks
```

- Apra
```bash
git checkout -b frontend_dashboard
```
### ৩. Coding

যত খুশি commit করতে পারো।
```bash
git add .
git commit -m "Add marks system"
```

### ৪. GitHub-এ Push
```bash
git push -u origin backend_marks

অথবা

git push -u origin frontend_dashboard
```
### ৫. Pull Request
```
GitHub
backend_marks
      ↓
Create Pull Request
      ↓
Merge into main
```

### ৬. Merge হওয়ার পরে

দুজনই
```bash
git checkout main
git pull origin main
```

### ৭. তারপর আবার নতুন Branch
```bash
main
   │
   ├── backend_attendance
   ├── frontend_student
   ├── backend_login
   ├── frontend_profile
   └── ...
```

## যেগুলো করবে না
- main branch-এ সরাসরি coding করবে না।
- একই branch (marks_system) মাসের পর মাস ব্যবহার করবে না।
- __pycache__, venv, database.db commit করবে না।
- git push --force ব্যবহার করবে না (শুধু বিশেষ পরিস্থিতিতে --force-with-lease ব্যবহার করা যায়)।

## Recommended Branch Strategy
```bash
main
│
├── backend_login
├── backend_marks
├── backend_attendance
├── frontend_dashboard
├── frontend_student
├── frontend_teacher
└── frontend_profile
```


## Note:
অর্থাৎ, একটি Feature = একটি Branch।

এতে:

Merge conflict অনেক কম হবে।
PR ছোট ও সহজ হবে।
কোনো feature-এ সমস্যা হলে শুধু সেই branch-টাই বাদ দিতে পারবে।
History পরিষ্কার থাকবে।

এটা GitHub Flow-এর খুব কাছাকাছি একটি workflow, যা ছোট টিম (২–১০ জন) এবং বেশিরভাগ সফটওয়্যার কোম্পানিতে ব্যাপকভাবে ব্যবহৃত হয়।