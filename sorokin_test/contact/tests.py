"""
    test contact
"""
from models import Person, RequestStore
from django.test import TestCase
from django.core.urlresolvers import reverse
from datetime import date
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


OTHER_USER = {'first_name': 'Vasia',
              'last_name': 'Pupin',
              'birthday': date.today(),
              'bio': 'molodec',
              'email': 'vasia@mail.com',
              'jabber': 'vasia@jabber.org',
              'skype': 'vasia',
              'other_contacts': 'tel: 123456'}


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
    model = Person
    fixture_count = 1
    field_list = ['id', 'first_name', 'last_name', 'birthday', 'bio', 'email',
                  'jabber', 'skype', 'other_contacts']


class TestModelRequestStore(TestModelBase, TestCase):
    model = RequestStore
    fixture_count = 0
    field_list = ['id', 'created', 'url', 'req_get', 'req_post', 'req_cookies',
                  'req_session', 'req_meta', 'res_status_code']


class TestPersonView(TestCase):
    url = reverse('person_detail')

    def setUp(self):
        self.person = Person.objects.all()[0]
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

    def test_both(self):
        Person.objects.all()[0].delete()
        Person.objects.create(**OTHER_USER)
        self.setUp()
        self.test_context()
        self.test_layout()


class TestLogin(TestCase):
    username = 'admin'
    password = 'admin'
    url = reverse('login')
    login_form = AuthenticationForm()

    def test_login(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        #check form is present
        for field in self.login_form:
            self.assertContains(response, field)
        #test with wrong password
        response = self.client.post(self.url,
                                    {'username': self.username,
                                     'password': '123'})
        self.assertEqual(response.status_code, 200)
        #test with valid password
        self.assertContains(response,
                            "Your username and password didn't match")

        response = self.client.post(self.url,
                                    {'username': self.username,
                                     'password': self.password})
        self.assertEqual(response.status_code, 302)


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


class TestPersonForm(TestCase):
    username = 'admin'
    password = 'admin'
    login_url = reverse('login')
    url = reverse('person_edit')
    main_url = reverse('person_detail')

    def setUp(self):
        self.person = Person.objects.all()[0]
        response = self.client.post(self.login_url,
                                    {'username': self.username,
                                     'password': self.password})
        self.assertEqual(response.status_code, 302)

    def test_layout(self):
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, self.person.last_name)
        self.assertContains(self.response, self.person.bio)

        self.person.last_name = 'Joe'
        self.person.save()

        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, self.person.last_name)
        self.assertContains(self.response, self.person.bio)

        self.response = self.client.post(self.url, OTHER_USER)
        self.assertEqual(self.response.status_code, 302)

        self.response = self.client.get(self.main_url)
        self.assertEqual(self.response.status_code, 200)

        self.assertContains(self.response, OTHER_USER['last_name'])
        self.assertContains(self.response, OTHER_USER['bio'])
