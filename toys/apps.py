from django.apps import AppConfig


class ToysConfig(AppConfig):
    name = 'toys'

    def ready(self):
        import toys.signals
