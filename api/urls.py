from django.urls import include, path
from .views import CategoryDetailView, CategoryListCreateView, CategoryListView, CategoryRetrieveUpdateDestroyView, CategoryViewSet, ProductListView, ProductViewSet, RegisterView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),  # <- добавили путь для регистрации
    # path('products/', ProductListView.as_view()),
    # path('categories/', CategoryListView.as_view()),
    # path('categories/<int:pk>/', CategoryDetailView.as_view()),  # <- добавили путь для работы с категориями
    # path('categories/', CategoryListCreateView.as_view()),  # <- добавили путь для работы с категориями
    # path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),  # <- добавили путь для работы с категориями
]
