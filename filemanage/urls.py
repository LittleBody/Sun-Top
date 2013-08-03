from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^delete/$', 'filemanage.views.delete'),
)
