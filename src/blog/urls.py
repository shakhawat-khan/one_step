from django.urls import path
from .views import PostListView,post_detail,PostCreateView,PostUpdateView,PostDeleteView,like_post

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', post_detail, name='post-detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/', like_post, name='like_post'),

]