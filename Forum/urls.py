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
        default_version=''
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui('swagger')),
    path('api/v1/', include('main.urls')),
    path('api/v1/account/', include('account.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
