from models import RequestStore
from django.views.generic import ListView


class RequestsListView(ListView):
    queryset = RequestStore.objects.all()[:10]
