from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import application

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^application/', include('application.urls', namespace='application')),
    url(r'^$', RedirectView.as_view(url='/application/', permanent=True)),
    #static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
