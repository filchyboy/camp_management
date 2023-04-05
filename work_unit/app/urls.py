from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('app.accounts.urls', namespace='accounts')),
    path('', include('app.work_unit.urls')),
    path('accounts/', include('allauth.urls')),
]
