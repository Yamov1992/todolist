
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'))),
    path('goals/', include(('todolist.goals.urls', 'todolist.goals'))),
    path("oauth/", include("social_django.urls", namespace="social")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),


]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'))
    ]
