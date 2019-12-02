from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', 'hackcollab_app.urls', name='www'),
    host(r'solarhacks', 'hackathon.urls', name='solarhacks'),
    host(r'testhacks', 'hackathon.urls', name='testhacks'),
    host(r'waycoolhacks', 'hackathon.urls', name='waycoolhacks'),
)
