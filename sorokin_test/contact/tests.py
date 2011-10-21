"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from models import Person

from django.test import TestCase


class TestModelPerson(TestCase):
    fixtures = ['mammals.json', 'birds']
    model = Person
    fixture_count = 1
    field_list = ['id', 'first_name', 'last_name', 'birthday', 'bio', 'email',
                  'jabber', 'skype', 'other_contacts']

    def setUp(self):
        self.objects_count = self.model.objects.count()
        self.field_list.sort()
        self.model_fields = [field.name for field in self.model_meta.fields]
        self.model_fields.sort()

    def test_fixture(self):
        self.assertEqual(self.objects_count, fixture_count)

    def test_fields(self):
        self.assertEqual(self.field_list, self.model_fields)
