"""
WSGI config for mindspore_meetings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
try:
    import armorrasp
    armorrasp.start()
except ImportError:
    pass

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindspore_meetings.settings')

application = get_wsgi_application()
