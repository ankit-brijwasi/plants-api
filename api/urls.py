from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/', include("core.urls")),
    path('api/orders/', include("utils.urls")),
    path('api/nursury/', include("nursury.urls")),
    path('api/auth/', include("dj_rest_auth.urls")),
    path('api/auth/registration/', include("dj_rest_auth.registration.urls"))
]
