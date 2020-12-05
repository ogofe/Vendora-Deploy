from django_hosts import patterns, host
from django.contrib.auth import urls
from django.urls import include


host_patterns = patterns('',
                         host(r'^$home', 'intro.urls', name='intro'),
                         host(r'^accounts$', include('accounts.urls', namespace='accounts'), name='core-auth'),
                         host(r'^$api$', include('api.urls', namespace='api-host'), name='api-host'),
                         host(r'^(?P<slug>)$', 'store.urls', name='store'),
                         host(r'^(?P<slug>).admin$', 'vendor.urls', name='vendor-admin'),
                         host(r'^super$', 'django.contrib.auth.urls', name='core-admin'),
                        )
                         