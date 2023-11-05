from django.contrib import admin
from django.urls import path, include
from views.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import TokenController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'token/',
        TokenController.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]


