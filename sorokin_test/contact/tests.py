"""
    test contact
"""
from sorokin_test.core.tests import TestModelBase
from models import Person
from django.test import TestCase
from django.core.urlresolvers import reverse
from datetime import date
from django.contrib.auth.forms import AuthenticationForm


OTHER_USER = {'first_name': 'Vasia',
              'last_name': 'Pupin',
              'birthday': date.today(),
              'bio': 'molodec',
              'email': 'vasia@mail.com',
              'jabber': 'vasia@jabber.org',
              'skype': 'vasia',
              'other_contacts': 'tel: 123456'}


class TestModelPerson(TestModelBase, TestCase):
    model = Person
    fixture_count = 1
    field_list = ['id', 'first_name', 'last_name', 'birthday', 'bio', 'email',
                  'jabber', 'skype', 'other_contacts']


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
