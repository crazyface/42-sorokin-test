from django import forms
from models import Person
from form_widgets import CalendarWidget


class PersonForm(forms.ModelForm):
    birthday = forms.DateField(widget=CalendarWidget)
    
    class Meta:
        model = Person
    
    class Media:
        js = ('js/edit_person.js',)

