from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^registe/$','account.views.registe'),
    url(r'^login/$','account.views.user_login'),
    url(r'^logout/$','account.views.user_logout'),
)
