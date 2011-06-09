from praktomat.configuration.models import Settings

def get_settings():
	return Settings.objects.get(id=1)