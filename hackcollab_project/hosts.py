from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', 'hackcollab_app.urls', name='www'),
    host(r'solarhacks', 'solarhacks.urls', name='solarhacks'),
)
