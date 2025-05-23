# Django News App

A content publishing platform where independent journalists and publishers collaborate to create and distribute articles. 
Readers can subscribe to individual journalists or entire publications, receive newsletters, and track content through personalized dashboards.

## Features

- Role-based access: Journalists, Publishers, Readers
- Article creation and editorial review system
- Publisher dashboards for content approvals
- Reader subscriptions to journalists and publishers
- Newsletter delivery and email notifications
- RESTful API for external access and integration

---

## Project Setup

You can run this project in two ways:

- Using a Python virtual environment
- Using Docker (recommended for deployment)

---

## Option 1: Run with Python Virtual Environment

### Requirements

- Python 3.11 or newer
- pip
- MySQL server installed locally
- MySQL client libraries (e.g. `mysqlclient` or `mysql-connector-python`)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/django-news-app.git
cd django-news-app

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

Configure MySQL Database
Before running migrations, update the DATABASES setting in settings.py:
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',  # Or your MySQL server host
        'PORT': '3306',       # Default MySQL port
    }
}
Replace 'your_database_name', 'your_mysql_user', and 'your_mysql_password' with your own MySQL credentials.

Final Steps
# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (admin account)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
Open http://127.0.0.1:8000 in your browser.

Option 2: Run with Docker
Requirements
Docker installed and running

Build and Run
# 1. Build the Docker image
docker build -t newsportal .

# 2. Run the Docker container
docker run -d -p 8000:8000 newsportal
Visit http://localhost:8000 in your browser.

If needed, you can run the app manually inside the container:
docker run -d -p 8000:8000 newsportal python manage.py runserver 0.0.0.0:8000
docker run -d -p 8000:8000 newsportal python manage.py runserver 0.0.0.0:8000
Running Tests
python manage.py test

Project Structure
django-news-app/
├── news/                   # Main Django app
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JavaScript)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker instructions
├── manage.py               # Django CLI entrypoint
└── README.md               # Project documentation
