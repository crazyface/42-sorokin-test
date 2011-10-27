from django.db import models
from django.core.urlresolvers import reverse
from sorokin_test.core.models import ModelMixIn 


class Person(ModelMixIn, models.Model):
    first_name = models.CharField('Name', max_length=35)
    last_name = models.CharField('Last name', max_length=35)
    birthday = models.DateField('Date of birth')
    bio = models.TextField('Bio')
    email = models.EmailField('E-mail')
    jabber = models.CharField('Jabber', max_length=35)
    skype = models.CharField('Skype', max_length=35)
    other_contacts = models.TextField('Other contacts')

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('person_detail')
