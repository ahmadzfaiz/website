from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.home'
    label = 'home'

    def ready(self):
        import project.home.signals
