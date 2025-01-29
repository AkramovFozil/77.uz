from django.urls import path
from . import views


urlpatterns = [
    path('store/categories/with/children/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('store/search/complete/', views.SearchAPIView.as_view(), name='search'),
    path('store/ads/create/', views.ProductCreateAPIView.as_view(), name='product_create'),
    path('store/ads/list/<str:category>/', views.ProductListAPIView.as_view(), name='product_list_by_category'),
    path('store/ads/list/', views.ProductListAPIView.as_view(), name='product_list'),
    path('store/ads/update/<slug:slug>/', views.ProductUpdateAPIView.as_view(), name='product_update'),
    path('store/ads/<slug:slug>/', views.ProductRetrieveAPIView.as_view(), name='product_detail'),
    path('store/ads/destroy/<slug:slug>/', views.ProductDestroyAPIView.as_view(), name='product_delete'),
    path('store/search/populars/', views.PopularSearchListAPIView.as_view(), name='search_popular'),
]
