from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet,basename='post')
router.register(r'categories', views.CategoryViewSet,basename='categories')
router.register(r'tags', views.TagViewSet,basename='tags')
router.register(r'user', views.UserAPI, basename='user-profile')

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-posts/', views.user_posts, name='user_posts'),
    
    path('', include(router.urls)),
]
