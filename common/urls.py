from django.urls import path
from .views import StaticPageRetrieveAPIView, RegionListAPIView


urlpatterns = [
    path('common/regions-with-districts/', RegionListAPIView.as_view(), name='region_list'),
    path('common/pages/<slug:slug>/', StaticPageRetrieveAPIView.as_view(), name='common_detail')
]