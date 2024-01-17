from django.urls import path
from .views import get_landing_image

urlpatterns = [
    # path('signup/', signup, name='signup'),
    # path('login/', login, name='login'),
    # path('login/', login, name='login'),
    path('landing-image/', get_landing_image, name='get_landing_image'),
]
