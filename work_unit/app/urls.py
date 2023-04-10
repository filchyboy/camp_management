from django.contrib import admin
from django.urls import path, include
from app.accounts.views import start_interview, add_tags, end_interview
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('app.accounts.urls', namespace='accounts')),
    path('', include('app.work_unit.urls')),
    path('accounts/', include('allauth.urls')),
    path('start_interview/', start_interview, name='start_interview'),
    path('add_tags/', add_tags, name='add_tags'),
    path('end_interview/', end_interview, name='end_interview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
