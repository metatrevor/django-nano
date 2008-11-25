from django import forms

from nano.privmsg.models import *

class PMForm(forms.ModelForm):
    class Meta:
        model = PM
        fields = ('text', 'subject')
