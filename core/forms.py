from django import forms
from core.models import NoticiesDocs

class NoticiesDocsForm(forms.ModelForm):
    class Meta:
        model = NoticiesDocs
        fields= ('notice', 'document', )
