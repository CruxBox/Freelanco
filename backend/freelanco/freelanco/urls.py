from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from .views import gettingStarted

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', TemplateView.as_view(template_name="social_app/index.html")),
	path('accounts/',include('users.urls')),
	#path('services/',include('services.urls')),


]

if settings.DEBUG:
	import debug_toolbar
	urlpatterns+=[path('__debug__/', include(debug_toolbar.urls))]
