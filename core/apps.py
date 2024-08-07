from django.apps import AppConfig
from jobs import *

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    def ready(self):
        from jobs import tasks
        tasks.start()