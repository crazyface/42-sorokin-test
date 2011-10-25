from django.views.generic import DetailView
from models import Person
from django.views.generic import UpdateView


class PersonDetailView(DetailView):
    context_object_name = "person"
    model = Person

    def get_object(self, **kwargs):
        return self.model.objects.all()[0]


class PersonEditView(UpdateView):
    model = Person

    def get_object(self, **kwargs):
        return self.model.objects.all()[0]


