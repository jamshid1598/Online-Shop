from django.urls import path

from django.contrib.auth import views as auth_view

from .views import (
    Product_List_View,
    # Category_Product_List_View,
    Product_Detail_View,
    Product_Create_View,
    Product_Update_View,
    Product_Delete_View,
)

app_name='Products'

urlpatterns = [
    # Product viewes' urls
    path('',                    Product_List_View.as_view(),   name='product-list'),
    path('<int:id>/category/',  Product_List_View.as_view(),   name='product-list'),
    path('<int:id>/detail/',    Product_Detail_View.as_view(), name='product-detail'),
    path('create/',             Product_Create_View.as_view(), name='product-create'),
    path('<int:id>/update/',    Product_Update_View.as_view(), name='product-update'),
    path('<int:id>/delete/',    Product_Delete_View.as_view(), name='product-delete'),
]
