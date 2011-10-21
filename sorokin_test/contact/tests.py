"""
    test contact
"""
from models import Person
from django.test import TestCase
from django.core.urlresolvers import reverse


class TestModelBase:
    """
    Base class for testing Model
    """
    #define this attrs when extend
    model = None
    fixture_count = None
    field_list = None

    def setUp(self):
        """
        Get object count
        Sort field name list
        """
        self.objects_count = self.model.objects.count()
        self.field_list.sort()

    def test_fixture(self):
        """
        Equal define object count with curren object count in db
        """
        self.assertEqual(self.objects_count, self.fixture_count)

    def test_fields(self):
        """
        Check model fields
        """
        self.assertEqual(self.field_list, self.model.fields_names())


class TestModelPerson(TestModelBase, TestCase):
    fixtures = ['person.json']
    model = Person
    fixture_count = 1
    field_list = ['id', 'first_name', 'last_name', 'birthday', 'bio', 'email',
                  'jabber', 'skype', 'other_contacts']


class TestPersonView(TestCase):
    fixtures = ['person.json']
    url = reverse('person_detail')

    def setUp(self):
        self.person = Person.objects.get(pk=1)
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)

    def test_context(self):
        context_person = self.response.context['person']
        self.assertEqual(str(context_person), str(self.person))

    def test_layout(self):
        self.assertContains(self.response, self.person.bio)
        self.assertContains(self.response, self.person.first_name)
        self.assertContains(self.response, self.person.jabber)
        self.assertContains(self.response, self.person.skype)
