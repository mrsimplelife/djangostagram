from typing import List, Union
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
import debug_toolbar
from django.urls.converters import register_converter
from django.views.generic.base import RedirectView
from django_pydenticon.views import image as pydenticon_image
from youme.converters import UsernameConverter

register_converter(UsernameConverter, "username")

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("admin/", admin.site.urls),
    path("identicon/image/<path:data>", pydenticon_image, name="pydenticon_image"),
    path("accounts/", include("accounts.urls")),
    path("instagram/", include("instagram.urls")),
    path("", RedirectView.as_view(pattern_name="instagram:index"), name="root"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
