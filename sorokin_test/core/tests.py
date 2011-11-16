from models import RequestStore
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings


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


class TestModelRequestStore(TestModelBase, TestCase):
    model = RequestStore
    fixture_count = 0
    field_list = ['id', 'created', 'url', 'req_get', 'req_post', 'req_cookies',
                  'req_session', 'req_meta', 'req_status_code']


class TestRequestView(TestCase):
    url1 = reverse('login')
    fake_url = '/asdas'
    url2 = reverse('requests')

    def test_context(self):
        # visit valid url
        self.response = self.client.get(self.url1)
        self.assertEqual(self.response.status_code, 200)

        #check that request is saved
        self.response = self.client.get(self.url2)
        self.assertContains(self.response, "/login/")
        self.assertContains(self.response, "200")

        #visit invalid url
        self.response = self.client.get(self.fake_url)
        self.assertEqual(self.response.status_code, 404)

        #check that request is saved
        self.response = self.client.get(self.url2)
        self.assertContains(self.response, self.fake_url)
        self.assertContains(self.response, "404")


class TestSettingsContextProc(TestCase):
    settings = settings
    url = reverse('login')

    def test_context(self):
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context['settings'],
                             self.settings)

        self.assertEqual(self.response.context['settings'].MEDIA_URL,
                             self.settings.MEDIA_URL)
        self.assertEqual(self.response.context['settings'].SECRET_KEY,
                             self.settings.SECRET_KEY)
