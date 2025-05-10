# 📰 Django Newsletter App

A web application built with Django that allows users to register, confirm their email, subscribe to a newsletter, and receive messages from the admin. Includes a secure admin panel for managing newsletters and subscribers.

---

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Security Notes](#security-notes)


---

## 🚀 Features

- 📨 **User registration with email confirmation**
- ✅ **Double opt-in newsletter subscription**
- 🗂️ **Admin panel for creating and sending newsletters**
- 📬 **Send newsletters to all confirmed and active subscribers**
- 🔒 **Sending limits to prevent spam**
- 🛡️ **MySQL database support (PythonAnywhere-ready)**
- ⚙️ **Secure .env configuration for secrets and credentials**

---

## 🖥️ Demo

*Demo coming soon!*

---

## 🛠️ Technologies

- **Python 3.10+**
- **Django 5.1.7**
- **HTML5**
- **CSS3**
- **MySQL**
- **SMTP (for email sending)**
- **Google Recaptcha**
- **Django-recaptcha**
- **python-dotenv** (for environment variables)

---

## 📁 Project Structure

Django-Newsletter-APP/
├── manage.py
├── requirements.txt
├── .env.example
├── newsletterpr/
│ ├── settings.py
│ ├── urls.py
│ └── ...
└── newsapp/
├── models.py
├── views.py
├── forms.py
├── templates/
│ ├── admin.html
│ ├── register.html
│ ├── confirm_email.html
│ └── ...
└── ...

text

---

## 📝 Installation Guide

### 1. Clone the repository

git clone https://github.com/Domino0D/Django-Newsletter-APP.git
cd Django-Newsletter-APP

text

### 2. Set up a virtual environment

python3 -m venv venv

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

text

### 3. Install dependencies

pip install -r requirements.txt

text

### 4. Configure environment variables

- Copy `.env.example` to `.env` and fill in your `SECRET_KEY`, database credentials, and email settings.

### 5. Run migrations

python manage.py migrate

text

### 6. Create a superuser (for admin access)

python manage.py createsuperuser

text

### 7. Collect static files

python manage.py collectstatic

text

### 8. Run the development server

python manage.py runserver

text

---

## ⚙️ Configuration

- **SECRET_KEY:** Set in your `.env` file for security.
- **Database:** MySQL recommended for production (PythonAnywhere-ready).
- **Email:** Configure SMTP in `.env` for sending confirmation and newsletter emails.
- **DEBUG:** Set to `False` in production.

---

## 🎮 Usage

### For Users
- Register at `/register/`
- Confirm your email via the link sent to your inbox
- Subscribe to the newsletter (even without registration)
- Receive newsletters when the admin sends them

### For Admins
- Log in to `/admin/` using your superuser credentials
- Create and send newsletters from the admin panel
- Manage subscribers and view their status

---

## 🖼️ Screenshots

*Add your screenshots here!*

---

## 🔒 Security Notes

- **Never commit your `.env` or sensitive keys to the repository.**
- **Always use strong, unique passwords for your superuser and database.**
- **Set `DEBUG = False` in production.**
- **Use HTTPS in production deployments.**
- **Change your SMTP/email credentials if you ever accidentally expose them.**

---

**Created with ❤️ by Domino0D**
