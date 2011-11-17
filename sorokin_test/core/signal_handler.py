from django.db.models.signals import post_delete, post_save
from models import DbEntry
from django.db.utils import DatabaseError

def post_save_handler(sender, instance, created, **kwargs):
    if not isinstance(instance, DbEntry) and hasattr(instance, 'id'):
        action = 'edit'
        if created:
            action = 'create'
        try:
            DbEntry.objects.create(action=action,
                                   content_object=instance,
                                   presentation=str(instance))
        except DatabaseError:
            pass
#    print sen./der, instance, created, kwargs

def post_delete_handler(sender, instance, **kwargs):
    if not isinstance(instance, DbEntry) and hasattr(instance, 'id'):
        try:
            DbEntry.objects.create(action='delete',
                                   content_object=instance,
                                   presentation=str(instance))
        except DatabaseError:
            pass

post_save.connect(post_save_handler)
post_delete.connect(post_delete_handler)