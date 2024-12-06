from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CodeFlowDeployed.content'

    def ready(self):
        import CodeFlowDeployed.content.signals