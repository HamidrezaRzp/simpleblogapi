from django.urls import path
from .views import ListPosts, DetailPost
urlpatterns = [
    path('postslist/', ListPosts.as_view(), name='postslist'),
    path('postdetail/<int:pk>', DetailPost.as_view(), name='postdetail'),
]
