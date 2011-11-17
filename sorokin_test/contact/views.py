from django.views.generic import DetailView
from models import Person
from django.views.generic import UpdateView
from forms import PersonForm

class PersonDetailView(DetailView):
    context_object_name = "person"
    model = Person

    def get_object(self, **kwargs):
        return self.model.objects.all()[0]


class PersonEditView(UpdateView):
#    model = Person
    form_class = PersonForm

    def get_object(self, **kwargs):
        return Person.objects.all()[0]
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'contact/form_content.html'
        return super(PersonEditView, self).post(request, args, kwargs)


