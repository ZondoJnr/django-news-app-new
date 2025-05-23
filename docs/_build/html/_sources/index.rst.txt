NewsPortal Documentation
========================

Welcome to the official documentation for the **NewsPortal Django Application**, a content publishing platform that enables collaboration between independent journalists and publishers, with features such as article management, subscription services, and personalized reader dashboards.

This documentation is intended to help developers understand the internal structure of the project, and how to set it up, configure, and extend it.

Getting Started
===============

**Project Overview:**

- Built with Django and Python 3.11+
- Role-based user system (Journalist, Publisher, Subscriber)
- Article writing, approval, and publishing system
- Email newsletters and reader subscriptions
- RESTful API support

**Setup Instructions:**

1. Clone the repository:
   ::

       git clone https://github.com/ZondoJnr/django-news-app-new.git

2. Navigate to the project directory and set up a virtual environment:
   ::

       cd django-news-app-new
       python -m venv venv
       venv\Scripts\activate

3. Install dependencies:
   ::

       pip install -r requirements.txt

4. Configure your MySQL database in `settings.py`:
   ::

       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.mysql',
               'NAME': 'your_db_name',
               'USER': 'your_db_user',
               'PASSWORD': 'your_db_password',
               'HOST': 'localhost',
               'PORT': '3306',
           }
       }

5. Apply migrations and start the server:
   ::

       python manage.py migrate
       python manage.py runserver


Modules
=======

Below are the available modules with documentation generated from the codebase:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
