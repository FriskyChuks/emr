from django.apps import AppConfig


class MedicalServicesConfig(AppConfig):
    name = 'medical_services'

    def ready(self):
        import medical_services.signals
