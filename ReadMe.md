# Django News App

A content publishing platform where independent journalists and publishers collaborate to create and distribute articles. 
Readers can subscribe to individual journalists or entire publications, receive newsletters, and track content through personalized dashboards.

## Features
- Journalist, Publisher, and Subscriber/Reader roles
- Article creation, editing, and review system
- Publisher dashboards and approvals
- Reader subscriptions to journalists and publishers
- Newsletters and email notifications
- RESTful API for external access

# NewsPortal Django Application

This is a Django-based news platform that supports independent journalists and publishers. The platform allows user role management, article publishing, subscriptions, and more.

---

## 🧰 Project Setup

You can run this project in two ways:

- Using a Python virtual environment (`venv`)
- Using Docker (recommended for deployment)

---

## 🐍 Option 1: Run with Virtual Environment

### ✅ Requirements

- Python 3.11+
- pip
- virtualenv (optional)

### 📦 Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/django-news-app.git
cd django-news-app

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver
````

---

## 🐳 Option 2: Run with Docker

### ✅ Requirements

* Docker installed and running

### 🏗️ Build and Run

```bash
# 1. Build the Docker image
docker build -t newsportal .

# 2. Run the container
docker run -d -p 8000:8000 newsportal

# 3. Visit your app
Open http://localhost:8000 in your browser
```

> ✅ **Note:** If the app doesn’t start automatically, run it manually:

```bash
docker run -d -p 8000:8000 newsportal python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📁 Project Structure

```
django-news-app/
├── news/                   # Main Django app
├── templates/              # HTML templates
├── static/                 # Static files (CSS/JS)
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
├── Dockerfile              # Docker build instructions
└── README.md               # This file
```