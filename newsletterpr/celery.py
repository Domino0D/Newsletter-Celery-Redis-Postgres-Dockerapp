import os 
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsletterpr.settings') # zmienna środowiskowa jako ustawienia apki django
app = Celery('newsletterpr') # aplikacja celery o nazwie takiej jak projekt django
app.config_from_object('django.conf:settings', namespace='CELERY') # ładuje konfig z settings aplikacji, szuka wierszy zaczynających sie od CELERY
app.autodiscover_tasks(['newsapp']) # automatycznie znajduje i rejestruje zadania (tasks.py) w apkach django
os.environ['CELERY_FORCE_EXECV'] = '1' # pomaga z odpalaniem na windows. na Linuxie z tym tot eż powinno działać