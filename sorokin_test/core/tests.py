from models import RequestStore
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from sorokin_test.core.templatetags.admin_urls import get_admin_url
from sorokin_test.contact.models import Person
from django.core.management import call_command
from sorokin_test.core.models import DbEntry
from datetime import date
from django.contrib.contenttypes.models import ContentType
import sys
from sorokin_test.core.utils import order_by
from sorokin_test.core.forms import RequestStoreEditList
from django.utils import simplejson


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
        if self.fixture_count:
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
                  'req_session', 'req_meta', 'req_status_code', 'priority']


class TestRequestView(TestCase):
    fixtures = ['request.json']
    login_url = reverse('login')
    fake_url = '/asdas'
    req_url = reverse('requests')

    def test_middleware(self):
        self.client.get(self.login_url)
        obj = RequestStore.objects.filter(url=self.login_url,
                                          req_status_code=200)
        self.assertEqual(obj.count(), 1)
        self.client.get(self.fake_url)
        obj = RequestStore.objects.filter(url=self.fake_url,
                                          req_status_code=404)
        self.assertEqual(obj.count(), 1)

    def test_context(self):
        # visit valid url
        self.response = self.client.get(self.login_url)
        self.assertEqual(self.response.status_code, 200)

        #check that request is saved
        self.response = self.client.get(self.req_url)
        self.assertContains(self.response, "/login/")
        self.assertContains(self.response, "200")

        #visit invalid url
        self.response = self.client.get(self.fake_url)
        self.assertEqual(self.response.status_code, 404)

        #check that request is saved
        self.response = self.client.get(self.req_url)
        self.assertContains(self.response, self.fake_url)
        self.assertContains(self.response, "404")

    def test_context_with_ordering(self):
        response = self.client.get(self.req_url + "?ordering=priority")
        prior_qs1 = response.context['object_list']
        prior_qs2 = RequestStore.objects.all().order_by('priority')[:10]
        self.assertEqual(list(prior_qs1), list(prior_qs2))

        response = self.client.get(self.req_url + "?ordering=-priority")
        reverse_qs1 = response.context['object_list']
        reverse_qs2 = RequestStore.objects.all().order_by('-priority')[:10]
        self.assertEqual(list(reverse_qs1), list(reverse_qs2))

        response = self.client.get(self.req_url)
        qs1 = response.context['object_list']
        qs2 = RequestStore.objects.all()[:10]
        self.assertEqual(list(qs1), list(qs2))

    def test_layout(self):
        response = self.client.get(self.req_url)
        self.assertContains(response, 'ordering=-priority')

        response = self.client.get(self.req_url + '?ordering=priority')
        self.assertContains(response, 'ordering=-priority')

        response = self.client.get(self.req_url + '?ordering=-priority')
        self.assertContains(response, '?ordering=priority')

    def build_post_request(self, queryset, formset_class):
        formset = formset_class(queryset=queryset)
        fields = {'form-TOTAL_FORMS': formset.total_form_count(),
                  'form-INITIAL_FORMS': formset.initial_form_count(),
                  'form-MAX_NUM_FORMS': ''}
        for form in formset:
            for field in form:
                fields[field.html_name] = field.value()
        return fields

    def test_formset(self):
        response = self.client.get(self.req_url)
        queryset = response.context['object_list']
        data = self.build_post_request(queryset, RequestStoreEditList)
        data['form-0-priority'] = 5
        obj_id = data['form-0-id']
        obj = RequestStore.objects.get(id=obj_id)
        before = obj.priority
        self.client.post(self.req_url, data=data)
        obj = RequestStore.objects.get(id=obj_id)
        after = obj.priority
        self.assertNotEqual(before, after)

    def test_ajax(self):
        obj = RequestStore.objects.all().order_by('?')[0]
        obj.priority = 1
        obj.save()
        response = self.client.post(self.req_url,
                                   {'id': obj.id, 'priority': 5},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        json_response = simplejson.loads(response.content)
        self.assertEqual(json_response['status'], 'success')

        #repick object
        obj = RequestStore.objects.get(id=obj.id)
        self.assertEqual(obj.priority, 5)

        response = self.client.post(self.req_url,
                                   {'priority': 5},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        json_response = simplejson.loads(response.content)
        self.assertEqual(json_response['status'], 'error')


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


class TestCustomTag(TestCase):

    def test_tag(self):
        obj = Person.objects.all()[0]
        self.assertEqual(get_admin_url(obj), '/admin/contact/person/1/')


class TestCustomCommand(TestCase):
    class Output():
        def __init__(self):
            self.text = ''

        def write(self, string):
            self.text = self.text + string

        def writelines(self, lines):
            for line in lines:
                self.write(line)

    def test_command(self):
        savestreams = sys.stdin, sys.stdout
        sys.stdout = self.Output()
        call_command('model_list')
        response = sys.stdout.text
        sys.stdin, sys.stdout = savestreams
        test_str = '%s has %s objects\n' % (RequestStore,
                                           RequestStore.objects.count())
        self.assertIn(test_str, response)


class TestDbEntry(TestModelBase, TestCase):
    model = DbEntry
    field_list = ['action', 'content_type', 'created', 'id',
                  'object_id', 'presentation']


class TestSignalsHandler(TestCase):

    def test_handler(self):
        data = {'first_name': 'Vasia',
                'last_name': 'Pupin',
                'birthday': date.today(),
                'bio': 'molodec',
                'email': 'vasia@mail.com',
                'jabber': 'vasia@jabber.org',
                'skype': 'vasia',
                'other_contacts': 'tel: 123456'}
        obj = Person.objects.create(**data)
        obj.first_name = 'Alex'
        obj.save()
        ctype = ContentType.objects.get_for_model(Person)
        Person.objects.filter(id=obj.id).delete()
        entries = DbEntry.objects.filter(content_type=ctype,
                                     object_id=obj.id)
        self.assertEqual(entries.filter(action='create').count(), 1)
        self.assertEqual(entries.filter(action='edit').count(), 1)
        self.assertEqual(entries.filter(action='delete').count(), 1)


class TestOrderBy(TestCase):

    def test_invert(self):
        order = order_by()
        self.assertEqual(order.invert('priority'), '-priority')
        self.assertEqual(order.invert('-created'), 'created')
        self.assertNotEqual(order.invert('url'), 'url')

    def test_querystring(self):
        order = order_by(allowed=['priority', 'date'])
        self.assertEqual(order.for_link('priority'),
                         'ordering=-priority')
        self.assertEqual(order.for_link('date'),
                         'ordering=-date')

        order = order_by(ordering=['-date'], allowed=['priority', 'date'])
        self.assertEqual(order.for_link('priority'),
                         'ordering=-priority&ordering=-date')
        self.assertEqual(order.for_link('date'),
                         'ordering=date')

        order = order_by(ordering=['-priority', 'date'],
                         allowed=['priority', 'date'])
        self.assertEqual(order.for_link('priority'),
                         'ordering=priority&ordering=date')
        self.assertEqual(order.for_link('date'),
                         'ordering=-date&ordering=-priority')
