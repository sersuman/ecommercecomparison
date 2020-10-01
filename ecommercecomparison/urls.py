
from django.contrib import admin
from django.urls import path
from core import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.UserCreate.as_view(), name='account-create'),
    path('additem', views.add_item, name='add-item'),
    path('item', views.get_item, name='get-item'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
