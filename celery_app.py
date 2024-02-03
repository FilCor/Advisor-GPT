from celery import Celery

# Assicurati che il nome del modulo sia corretto e che sia riconoscibile nel PYTHONPATH
celery_app = Celery(
    "analysis_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.autodiscover_tasks(['tasks'], force=True)