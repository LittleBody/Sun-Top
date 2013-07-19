from django.conf.urls import patterns, include, url

#from base import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'suntop.views.home', name='home'),
    # url(r'^suntop/', include('suntop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$','base.views.helloView'),
    url(r'^account/',include('account.urls')),
    url(r'^filemanage/',include('filemanage.urls')),
)


