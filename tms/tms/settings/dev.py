from tms.settings.base import *

CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL')
TODOS_URL = os.environ.get('TODOS_URL')
TERMS_OF_SERVICE = os.environ.get('TERMS_OF_SERVICE')

INSTALLED_APPS = [
                     'debug_toolbar',
                     'drf_yasg',
                     'django_extensions'
                 ] + INSTALLED_APPS

MIDDLEWARE = [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
                 'posts.middleware.middleware_todo.QueryLogsMiddleware',
             ] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1', ]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def show_toolbar(request):
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'tms.settings.dev.show_toolbar',
}
