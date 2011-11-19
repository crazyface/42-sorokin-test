from models import RequestStore
from django.views.generic import ListView
from sorokin_test.core.utils import order_by
from sorokin_test.core.forms import RequestStoreEditList
from django.http import HttpResponseRedirect


class RequestsListView(ListView):
    model = RequestStore
    formset_class = RequestStoreEditList

    def get_context_data(self, **kwargs):
        context = super(RequestsListView, self).get_context_data(**kwargs)

        get = dict(self.request.GET)
        self.order = order_by(get.get('ordering', []), ['priority'])
        context['order'] = self.order

        queryset = context['object_list']
        if self.order.ordering:
            queryset = queryset.order_by(*self.order.ordering)
        queryset = queryset[:10]

        context['object_list'] = queryset
        context['formset'] = self.formset_class(queryset=queryset)
        return context

    def get_succes_url(self):
        return self.request.path + '?' + self.order.get_current_order()

    def post(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        formset = self.formset_class(self.request.POST)
        context['formset'] = formset
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(self.get_succes_url())
        return self.render_to_response(context)
