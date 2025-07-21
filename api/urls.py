from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet,basename='post')
router.register(r'categories', views.CategoryViewSet,basename='categories')
router.register(r'tags', views.TagViewSet,basename='tags')

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.UserRegistrationView.as_view(), name='user_register'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('my-posts/', views.user_posts, name='user_posts'),
    
    path('', include(router.urls)),
]
