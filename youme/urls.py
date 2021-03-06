from typing import List, Union
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import TemplateView
import debug_toolbar
from django_pydenticon.views import image as pydenticon_image

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("admin/", admin.site.urls),
    path("identicon/image/<path:data>", pydenticon_image, name="pydenticon_image"),
    path(
        "", login_required(TemplateView.as_view(template_name="root.html")), name="root"
    ),
    path("accounts/", include("accounts.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
