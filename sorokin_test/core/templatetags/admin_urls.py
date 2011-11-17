from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag
def get_admin_url(obj):
    try:
        return reverse('admin:' + obj._meta.db_table + '_change',
                       args=(obj.id,))
    except:
        return obj 
    