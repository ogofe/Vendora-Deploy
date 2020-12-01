from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('', include('intro.urls', namespace='base')),
    path('api/', include('api.urls', namespace='api')),
    path('<str:store_name>/admin/', include('vendor.urls', namespace='vendor')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('store/', include('store.urls', namespace='store')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)