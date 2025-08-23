from django.urls import path
from blogs import views

urlpatterns = [
    path('create-post/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create-comment/<int:post_id>/', views.CreateCommentView.as_view(), name='create_comment'),
]
