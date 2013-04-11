from django.forms.models import ModelForm
from registry.models import Entry
from django.forms.widgets import Textarea, TextInput
from django.forms.fields import CharField
#from tinymce.widgets import TinyMCE #@UnresolvedImport

class AddEntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ('scrape_id', 'ip', 'entry_flag')
        widgets = {
            'car': TextInput(),
            'comments': Textarea(attrs={'rows': 7, 'cols': 120, 'maxLength': 10000}),
            #'comments': TinyMCE(attrs={'rows': 7, 'cols': 120, 'maxLength': 10000}),
            'mileage': TextInput(attrs={'size': 10 }),
            #'miles': CharField(widget=TextInput(attrs={'class': 'mileage'})),
            
        }
