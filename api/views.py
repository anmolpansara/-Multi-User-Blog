from rest_framework import generics, permissions, filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Post, Category, Tag, UserProfile
from .serializers import (
    UserRegistrationSerializer, PostSerializer, PostListSerializer,
    CategorySerializer, TagSerializer, UserProfileSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly, 
    CanCreatePost, CanViewPublishedOnly
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.userprofile

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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)
