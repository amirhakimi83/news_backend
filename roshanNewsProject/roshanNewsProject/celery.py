from celery import Celery
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roshanNewsProject.settings')

app = Celery('roshanNewsProject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
