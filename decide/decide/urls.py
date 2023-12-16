from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


schema_view = get_swagger_view(title='Decide API')

urlpatterns = [
    path('i18n/', include("django.conf.urls.i18n")),
]

urlpatterns +=  i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('doc/', schema_view),
    path('gateway/', include('gateway.urls')),
    path('', include('comentarios.urls')),
    path('', include('base.urls')),
    path('', include('core.urls')),
    path('accounts/' , include('allauth.urls')),
)


for module in settings.MODULES:
    urlpatterns += [
        path('{}/'.format(module), include('{}.urls'.format(module)))
    ]
