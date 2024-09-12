from django.contrib import admin
from django.urls import path

# from django.conf import settings
# from django.conf.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from rest_framework.routers import DefaultRouter

from gpa_calculator.views import GPAViewSet, Register

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="CRM Django",
        default_version='v1', ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('gpa', GPAViewSet, basename='gpa')
router.register('account', Register, basename='account')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
