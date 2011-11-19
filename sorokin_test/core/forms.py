from django.forms.models import modelformset_factory
from django import forms
from sorokin_test.core.models import RequestStore


class RequestStoreForm(forms.ModelForm):
    class Meta:
        fields = ('priority',)
        model = RequestStore


RequestStoreEditList = modelformset_factory(RequestStore,
                                            form=RequestStoreForm,
                                            extra=0)
