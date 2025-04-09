from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Category, Product
from api.permissions import IsOwnerOrReadOnly
from api.serializers import CategorySerializer, ProductSerializer, RegisterSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()                         # <- получили ВСЕ продукты из базы
        serializer = ProductSerializer(products, many=True)      # <- преобразовали их в JSON
        return Response(serializer.data)                          # <- вернули результат клиенту

    def post(self, request):
        serializer = ProductSerializer(data=request.data)       # <- создали сериализатор
        if serializer.is_valid():
            serializer.save()                                    # <- сохраняем в базу
            return Response(serializer.data, status=status.HTTP_201_CREATED)         # <- вернули результат клиенту
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           # <- вернули ошибку клиенту
    
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Using Django Rest Framework's generic views 
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # <- доступ только для авторизованных пользователей
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # фильтрация, поиск и сортировка
    filterset_fields = ['category'] # фильтрация по полям
    search_fields = ['name', 'description'] # поиск (поиск по частичному совпадению)
    ordering_fields = ['price', 'name'] # сортировка по полям

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Using Django Rest Framework's viewsets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # <- доступ только для авторизованных пользователей
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']  # фильтрация по полям
    search_fields = ['name']     # поиск (поиск по частичному совпадению)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully'        
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
