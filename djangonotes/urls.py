from django.conf.urls import patterns, include, url

urlpatterns = patterns('djangonotes.views',
url(r'^$', 'index', name='index'),
url(r'^create/$', 'create', name='create'),
url(r'^edit/(?P<note_id>\d+)/$', 'edit', name='edit'),
)

