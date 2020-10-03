from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserCreate.as_view(), name='account-create'),
    path('item/add', views.add_item, name='add-item'),
    path('item', views.get_item, name='get-item'),
    path('scrape', views.get_content, name='scrape'),
]