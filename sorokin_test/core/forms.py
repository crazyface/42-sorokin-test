from django.forms.models import modelformset_factory
from sorokin_test.core.models import RequestStore


RequestStoreEditList = modelformset_factory(RequestStore,
                                            fields=('priority',),
                                             extra=0)
