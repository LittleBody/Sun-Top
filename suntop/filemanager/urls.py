from django.conf.urls import patterns,include,url

urlpatterns = patterns('',
    url(r'^upload/(?P<path>.*)', 'upload', name='fileserver_upload'),
)
