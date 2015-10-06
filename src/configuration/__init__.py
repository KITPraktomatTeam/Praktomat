def get_settings():
    from configuration.models import Settings
    return Settings.objects.get(id=1)
