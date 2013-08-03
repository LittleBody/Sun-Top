from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^delete/$', 'filemanage.views.delete'),
    url(r'^myshare/$', 'filemanage.views.my_share'),
    url(r'^share/$', 'filemanage.views.all_share'),
)
