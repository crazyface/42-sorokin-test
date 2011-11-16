from django.core.management.base import BaseCommand, CommandError
from django.db import models

class Command(BaseCommand):
#    args = '<poll_id poll_id ...>'
#    help = 'Closes the specified poll for voting'
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.models = models.get_models()

    def handle(self, *args, **options):
        for model in self.models:
#            try:
#                poll = Poll.objects.get(pk=int(poll_id))
#            except Poll.DoesNotExist:
#                raise CommandError('Poll "%s" does not exist' % poll_id)
#
#            poll.opened = False
#            poll.save()
            self.stdout.write('%s has %s objects\n ' % (model, model.objects.count()))