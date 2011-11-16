from django.core.management.base import BaseCommand, CommandError
from django.db import models

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        model_list = []
        if args:
            for arg in args:
                model_list.append(models.get_model(*arg.split('.')))
        else:
            model_list = models.get_models()
        for model in model_list:
            self.stdout.write('%s has %s objects\n' % (model, model.objects.count()))