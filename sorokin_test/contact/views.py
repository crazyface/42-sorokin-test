from django.views.generic import DetailView
from models import Person


class PersonDetailView(DetailView):
    context_object_name = "person"
    model = Person

    def get_object(self, **kwargs):
#        self.kwargs['pk'] = 1
#        obj = super(PersonDetailView, self).get_object()
        return self.model.objects.all()[0]
