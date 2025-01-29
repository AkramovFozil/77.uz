from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers, models, paginations


class AuthorValidateProductAPIView(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.seller


class CategoryListAPIView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name', '=parent']

    # @action(detail=False, methods=['get'])
    # def product_list(self, request):
    #     categories = models.Product.objects.values('category').distinct()
    #
    #     products = []
    #
    #     for category in categories:
    #         product = models.Product.objects.filter(category=category['category']).order_by('-published_at').first()
    #         if product:
    #             products.append(product)
    #
    #     serializer = serializers.ProductForGetSerializer(products, many=True)
    #     return Response(serializer.data)


class ProductListAPIView(ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductForGetSerializer
    pagination_class = paginations.ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'price', 'address', 'category', 'published_at']
    filterset_fields = ['price', 'address', 'published_at', 'category', 'currency']
    ordering_fields = ['category']
    ordering = ['category']

    # def get_queryset(self):
    #     category = self.kwargs.get('category')
    #     if category:
    #         products = models.Product.objects.filter(category__name=category)
    #         if products.exists():
    #             return products
    #         return models.Product.objects.none()
    #     return models.Product.objects.all()


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductForGetSerializer

class ProductCreateAPIView(CreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductUpdateAPIView(UpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [AuthorValidateProductAPIView]


class ProductDestroyAPIView(DestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductForGetSerializer
    permission_classes = [AuthorValidateProductAPIView]


class SearchAPIView(APIView):
    queryset = models.Product.objects.all()

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)

        if search_query is None:
            posts = self.queryset
        else:
            word = models.PopularSearchWord.objects.filter(word=search_query)
            if word:
                word.count += 1
                word.save()
            else:
                models.PopularSearchWord.objects.create(word=search_query, count=1)
            search_filter = Q(
                name__icontains=search_query
            ) | Q(
                price__icontains=search_query
            ) | Q(
                currency__icontains=search_query
            ) | Q(
                published_at__icontains=search_query
            ) | Q(
                category__name__icontains=search_query
            ) | Q(
                category__parent__name__icontains=search_query
            ) | Q(
                category__parent__parent__name__icontains=search_query
            )

            posts = self.queryset.filter(search_filter)

        serializer = serializers.ProductSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularSearchListAPIView(ListAPIView):
    queryset = models.PopularSearchWord.objects.all()
    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.PopularSearchWord.objects.all().order_by('-count')[:3]
