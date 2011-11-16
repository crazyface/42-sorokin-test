from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        model_list = []
        for arg in args:
            model_list.append(models.get_model(*arg.split('.')))
        if not model_list:
            model_list = models.get_models()
        for model in model_list:
            self.stdout.write('%s has %s objects\n' % (model,
                                                       model.objects.count()))
