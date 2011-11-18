from models import RequestStore
from django.views.generic import ListView
from sorokin_test.core.utils import order_by


class RequestsListView(ListView):
    model = RequestStore

    def get_context_data(self, **kwargs):
        context = super(RequestsListView, self).get_context_data(**kwargs)
        get = dict(self.request.GET)
        order = order_by(get.get('ordering', []), ['priority'])
        context['order'] = order
        q = context['object_list']
        if order.ordering:
            q = q.order_by(*order.ordering)
        context['object_list'] = q[:10]
        return context
