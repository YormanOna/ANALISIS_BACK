from django.apps import AppConfig

class BananasCoctailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bananas_coctails'

    def ready(self):
        from importlib import import_module
        import_module('bananas_coctails.signals')

