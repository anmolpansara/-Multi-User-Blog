from rest_framework import generics, permissions, filters, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Post, Category, Tag
from .serializers import (
    UserSerializer, PostSerializer, PostListSerializer,
    CategorySerializer, TagSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly, 
    CanCreatePost, CanViewPublishedOnly
)

class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status_code': 200,
            'message': 'Users retrieved successfully'
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'status_code': 200,
            'message': 'User retrieved successfully'
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'data': serializer.data,
            'status_code': 201,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status_code': 200,
            'message': 'User updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status_code': 200,
            'message': 'User deleted successfully',
            'data': None
        })
   
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreatePost]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags', 'status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'published_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'userprofile'):
            if user.userprofile.role in ['admin', 'editor']:
                return Post.objects.all()
            else:  # reader
                return Post.objects.filter(status='published')
        return Post.objects.filter(status='published')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'retrieve']:
            return PostSerializer
        return PostListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly, CanViewPublishedOnly]
        else:
            permission_classes = [permissions.IsAuthenticated, CanCreatePost]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'status_code': 200,
                'message': 'Posts retrieved successfully',
                'data': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': 200,
            'message': 'Posts retrieved successfully',
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status_code': 200,
            'message': 'Post retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status_code': 201,
            'message': 'Post created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status_code': 200,
            'message': 'Post updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status_code': 200,
            'message': 'Post deleted successfully',
            'data': None
        })
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': 200,
            'message': 'Categories retrieved successfully',
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status_code': 200,
            'message': 'Category retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status_code': 201,
            'message': 'Category created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status_code': 200,
            'message': 'Category updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status_code': 200,
            'message': 'Category deleted successfully',
            'data': None
        })

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': 200,
            'message': 'Tags retrieved successfully',
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status_code': 200,
            'message': 'Tag retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status_code': 201,
            'message': 'Tag created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status_code': 200,
            'message': 'Tag updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status_code': 200,
            'message': 'Tag deleted successfully',
            'data': None
        })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    serializer = PostListSerializer(posts, many=True)
    return Response({
        'status_code': 200,
        'message': 'User posts retrieved successfully',
        'data': serializer.data
    })
