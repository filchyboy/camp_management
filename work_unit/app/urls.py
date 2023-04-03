from django.contrib import admin
from django.urls import path, include
# No need to import homepage here, since you'll include the work_unit app's URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('app.accounts.urls')),
    # Include the work_unit app's URLs
    path('', include('app.work_unit.urls')),
]
