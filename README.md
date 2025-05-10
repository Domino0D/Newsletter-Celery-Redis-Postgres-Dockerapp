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

https://dominoo.pythonanywhere.com/ (for non-admin users only!)

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

```plaintext
Django-Newsletter-APP/
├── manage.py
├── requirements.txt
├── .env.example
├── newsletterpr/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── newsapp/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── templates/
    │   ├── admin.html
    │   ├── register.html
    │   ├── confirm_email.html
    │   └── ...
    └── ...
```

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

🛡️ Google reCAPTCHA Integration
Protect your forms from bots using Google reCAPTCHA.

Register and Get Keys
Go to Google reCAPTCHA Admin Console

Choose reCAPTCHA v2 ("I'm not a robot" Checkbox)

Add your domains (e.g., localhost, yourapp.pythonanywhere.com)

Copy your Site Key and Secret Key

Install Django reCAPTCHA
bash
pip install django-recaptcha
Add to your INSTALLED_APPS in settings.py:

python
'django_recaptcha',
Configure Keys
Add to your .env file:

text
RECAPTCHA_PUBLIC_KEY=your_site_key
RECAPTCHA_PRIVATE_KEY=your_secret_key
And load them in settings.py:

python
import os
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
Use in Forms
In your forms.py:

python
from django_recaptcha.fields import ReCaptchaField

class RegisterForm(forms.Form):
    # ... your fields ...
    captcha = ReCaptchaField()
Render in Template
In your template (e.g. register.html):

text
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
The reCAPTCHA widget will appear automatically.

Tips
For local testing, add localhost and 127.0.0.1 as allowed domains in Google reCAPTCHA settings.

Never commit your real keys to the repository – use your .env file!

If you get validation errors, check your keys and domain settings.

More Info
django-recaptcha documentation

Po wklejeniu na GitHubie nagłówki będą widoczne jako sekcje, a całość będzie czytelna i zgodna z resztą README!
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

## 🔒 Security Notes

- **Never commit your `.env` or sensitive keys to the repository.**
- **Always use strong, unique passwords for your superuser and database.**
- **Set `DEBUG = False` in production.**
- **Use HTTPS in production deployments.**
- **Change your SMTP/email credentials if you ever accidentally expose them.**

---

**Created with ❤️ by Domino0D**
