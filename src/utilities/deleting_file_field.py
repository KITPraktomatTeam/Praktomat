from django.db import models
from django.db.models import signals

class DeletingFileField(models.FileField):
    """ FileField subclass that deletes the referenced file when the model object itself is deleted. This was the default behavior in django 1.2 but was dropped in 1.2.5 because of possible data loss in rollbacks or if you referenced the file in another model. Changing the file will non the less leave orphaned files."""
    def contribute_to_class(self, cls, name):
        super(DeletingFileField, self).contribute_to_class(cls, name)
        signals.post_delete.connect(self.delete_file, sender=cls)

    def delete_file(self, instance, sender, **kwargs):
        file = getattr(instance, self.attname)
        # If no other object of this type references the file,
        # and it's not the default value for future objects,
        # delete it from the backend.
        if file and file.name != self.default and \
            not sender._default_manager.filter(**{self.name: file.name}):
            file.delete(save=False)
        elif file:
            # Otherwise, just close the file, so it doesn't tie up resources.
            file.close()
