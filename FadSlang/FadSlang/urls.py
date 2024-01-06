from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("api.auth.urls")),
    path("api/dashboard/", include("api.dashboard.urls")),
    path("api/products/", include("api.products.urls")),
]