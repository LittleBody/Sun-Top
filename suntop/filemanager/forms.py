from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy, ugettext as _
from django.core.files.storage import default_storage


class UploadForm(forms.Form):
    name = forms.fields.FileField()
