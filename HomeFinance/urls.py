from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^userauth/', include('userauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('Finance.urls')),
    # url(r'^blog/', include('blog.urls')),


)
