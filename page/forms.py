from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat


from django import forms


class UploadForm(forms.Form):
    filename = forms.CharField(max_length=100)
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )