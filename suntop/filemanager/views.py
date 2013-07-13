# Create mport os
from StringIO import StringIO
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, View, RedirectView
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
from django.contrib import messages
from django.views.defaults import page_not_found

from extra_views import FormSetView

from .utils.filesystem import Directory, guess_type
from .utils.views import LogedInMixin, SetPathMixin
from .forms import (UploadForm,)

#upload the file and photo
class UploadView(SetPathMixin, LogedInMixin, FormSetView):
    form_class = UploadForm
    template_name = 'filemanager/templates/upload.html'
    extra = 3

    def get(self, request, *args, **kwargs):
        messages.warning(self.request, _('Do not reload this page!'))
        return super(UploadView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('fileserver_browse', args=[self.get_path()])
    #在formset_valid中进行POST请求的处理，(其父类format_valid做一个成功跳转工作)
    
    def formset_valid(self, formset):
        path = self.get_path()
        for form in formset:
            if 'file' in form.cleaned_data:
                file_name = os.path.join(path, form.cleaned_data['file'].name)
                default_storage.save(file_name, form.cleaned_data['file'])
        return super(UploadView, self).formset_valid(formset)
upload = UploadView.as_view()


#Browse the file and photo 
class BrowseView(SetPathMixin, LogedInMixin, TemplateView):
    template_name = 'filemanager/templates/browse.html'

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        path = self.get_path()
        sort = self.request.GET.get('sort', self.request.session.get('sort', 'name'))
        reverse = self.request.GET.get(
            'reverse', self.request.session.get('reverse', False))
        if reverse == 'false' or reverse == '0':
            reverse = False
        else:
            reverse = bool(reverse)
        self.request.session['sort'] = sort
        self.request.session['reverse'] = reverse
        context['directory'] = Directory(path, sort=sort, reverse=reverse)

        reverse = 'false' if reverse else 'true'
        context['name_url'] = "?sort=name"
        context['size_url'] = "?sort=size"
        key = {'name': 'name_url', 'size': 'size_url'}[sort]
        context[key] += "&reverse=%s" % reverse
        return context

browse = BrowseView.as_view()









