from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title='Forum FF',
        description='Fanfic forum',
        default_version='api/v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vi/docs/', schema_view.with_ui('swagger')),
    path('api/vi/', include('main.urls')),
    path('api/vi/account/', include('account.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
