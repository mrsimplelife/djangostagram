from typing import Union
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import TemplateView
import debug_toolbar

urlpatterns: list[Union[URLPattern, URLResolver]] = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='root.html'), name='root')
]
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
