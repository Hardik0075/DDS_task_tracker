# DDS Task Tracker: Centralized Operational Workflows

DDS Task Tracker is a centralized operational workflow tracking web application engineered for technical teams managing vendor and product data extraction tasks. This system is designed as a Django monolith using Bootstrap 5, PostgreSQL (Neon DB), Gunicorn, and WhiteNoise.

---

## 1. Directory Structure

```
DDS_task_tracker/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── render.yaml
├── .gitignore
├── .env.example
├── README.md
├── task_tracker/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/
│       ├── base.html
│       ├── registration/
│       │   └── login.html
│       └── tasks/
│           ├── dashboard.html
│           ├── task_confirm_delete.html
│           ├── task_detail.html
│           ├── task_form.html
│           ├── task_list.html
│           ├── user_edit.html
│           └── user_management.html
└── static/
    └── css/
        └── styles.css
```

---

## 2. Local Development Setup

To configure the application locally, follow these steps:

### Step 2.1: Clone/Prepare Directory
Open a terminal in the root `DDS_task_tracker` directory.

### Step 2.2: Establish Virtual Environment
Create and activate a Python virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2.3: Install Dependencies
Install all package requirements:
```bash
pip install -r requirements.txt
```

### Step 2.4: Create `.env` configuration file
Duplicate `.env.example` to create a `.env` file:
```bash
# Windows (PowerShell)
copy .env.example .env

# macOS / Linux / Windows (CMD)
cp .env.example .env
```
Open `.env` and configure:
- `SECRET_KEY`: Set a secure secret key.
- `DEBUG`: Set to `True` for local development.
- `DATABASE_URL`: Add your Neon database string or omit to automatically fall back to local `db.sqlite3` for testing.

---

## 3. Neon DB Connection Setup

The project is pre-configured to parse standard PostgreSQL database connection URLs.

To use Neon DB:
1. Log in to your [Neon Console](https://console.neon.tech/).
2. Retrieve your connection string from the Dashboard. It will look like this:
   `postgresql://neondb_owner:YOUR_NEW_PASSWORD@ep-proud-mouse-aozqc24u-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`
3. Paste this string directly into your `.env` file under `DATABASE_URL=...` (replace `YOUR_NEW_PASSWORD` with your actual password).

---

## 4. Run Migrations & Setup Superuser

Once your database is configured:

### Step 4.1: Perform Migrations
Create and execute migrations on the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4.2: Create Superuser (Admin)
Register the first Admin user account:
```bash
python manage.py createsuperuser
```
Follow the prompts (Username, Email, Password). 

*Note: Since standard user management maps **Admins** to `is_staff` / `is_superuser`, creating a superuser provides full CRUD permissions over all task and user management pages.*

### Step 4.3: Launch Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000` to log in with your superuser account.

---

## 5. User Roles and Security

The system implements Role-Based Access Controls (RBAC):

1. **Admin (Superuser / Staff)**:
   - Full Create, Read, Update, Delete (CRUD) operations on Tasks.
   - User account directory management (Create accounts, update roles, toggle active status).
   - Add workflow commentary to Task details.
2. **Read-Only**:
   - Access to the Dashboard and Task Inventory list.
   - Run keyword searches, sort columns, and apply filter criteria.
   - Open and view task parameters, comments history, and notes.
   - Cannot create, modify, delete tasks or post updates.

---

## 6. GitHub Push Instructions

To upload this workspace to your GitHub repository:

```bash
# Initialize git repository
git init

# Add all files to staging index
git add .

# Create initial commit
git commit -m "Initialize central DDS task tracker project"

# Link your remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename default branch to main
git branch -M main

# Push code to remote repository
git push -u origin main
```

---

## 7. Render Deployment Instructions

This project includes pre-configured `Procfile`, `runtime.txt`, and `render.yaml` blueprints for instant hosting on Render.

### Step 7.1: Register on Render
Create an account on [Render](https://render.com/) and link your GitHub account.

### Step 7.2: Import Blueprint
1. Click **New +** and select **Blueprint**.
2. Select your repository containing this task tracker project.
3. Render will read `render.yaml` and configure:
   - Python 3.11 environment.
   - Install packages from `requirements.txt`.
   - Compile static resources via `collectstatic`.
   - Run initial migrations to your Neon database.
4. Input your `DATABASE_URL` environment variable if prompted.

### Step 7.3: Finish Deploy
Once the blueprint build finishes, your site URL will be generated (e.g. `https://dds-task-tracker.onrender.com`). Open this URL to log in.
