from rest_framework.generics import ListAPIView, RetrieveAPIView
from . import serializers, models


class RegionListAPIView(ListAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionListSerializer


class StaticPageRetrieveAPIView(RetrieveAPIView):
    queryset = models.StaticPage.objects.all()
    serializer_class = serializers.StaticPageSerializer

