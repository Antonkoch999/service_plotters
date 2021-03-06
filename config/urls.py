from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = i18n_patterns(
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("main_service_of_plotters.apps.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
    # Your stuff: custom urls includes go here
    path("tickets/", include("main_service_of_plotters.apps.ticket.urls", namespace="tickets")),

 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs without i18n
urlpatterns += [
    path("acra/", include("main_service_of_plotters.apps.acra.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name='schema'),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path("api/schema/redoc/", SpectacularRedocView.as_view(), name='redoc'),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    # path("auth-token/", obtain_auth_token),
    # JWT auth token
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    # FIXME api auth methods
    path('api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework'
    )),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
