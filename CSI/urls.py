from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('apiserv.urls')),
]

# Remove in production
if True:
    urlpatterns.append(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
