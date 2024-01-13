from django.urls import path
from .views import *

urlpatterns = [
    path('product/',product, name='product'),
    path('categories/',categories, name='categories'),
    path('categories-home/',categorieshome, name='categorieshome'),
    # path('login/', login, name='login'),
]
