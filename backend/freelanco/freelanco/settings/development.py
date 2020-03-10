from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS +=[
        'debug_toolbar',
]

MIDDLEWARE +=[
        'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# Debug toolbar configuration

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
    #'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar
}

#client_id=27002450847-jposhfmk76db203osbpshhulminfk052.apps.googleusercontent.com
#secret_key=Bf0E_PPadIggLWfTFQ5PacCF