from django.views.generic import DetailView
from models import Person, RequestStore
from django.views.generic import TemplateView, ListView


class PersonDetailView(DetailView):
    context_object_name = "person"
    model = Person

    def get_object(self, **kwargs):
        return self.model.objects.all()[0]


class RequestsListView(ListView):
    queryset = RequestStore.objects.all()[:10]
