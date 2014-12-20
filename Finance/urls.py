#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.conf import settings


urlpatterns = patterns('Finance',

     url(r'dettaglio_cdc/(?P<cdc_id>\d{1,10})/', 'views.dettaglio_cdc', name='dettaglio_cdc'),

     url(r'modifica_movimento/(?P<movimento_id>\d{1,10})/', 'views.modifica_movimento', name='modifica_movimento'),

     url(r'new_movimento/(?P<cdc_id>\d{1,10})/', 'views.new_movimento', name='new_movimento'),
     url(r'new_movimento/', 'views.new_movimento', name='new_movimento'),

     url(r'elenco_gruppi/', 'views.elenco_gruppi', name='elenco_gruppi'),

     url(r'ultimi_movimenti/', 'views.ultimi_movimenti', name='ultimi_movimenti'),

     url(r'fornitori/', 'views.fornitori', name='fornitori'),

     url(r'^$', 'views.index', name='home'),

     )

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)