from django import forms


class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('css/flora.datepicker.css',)
        }
        js = ('js/ui.core.js', 'js/ui.datepicker.js')