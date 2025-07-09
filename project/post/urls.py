from django.urls import path
from .views import UserViewset, PostViewset
from rest_framework.routers import SimpleRouter

'''
urlpatterns = [
    path('postslist/', ListPosts.as_view(), name='postslist'),
    path('postdetail/<int:pk>', DetailPost.as_view(), name='postdetail'),
]
'''

router = SimpleRouter()

router.register('user', UserViewset, basename='user')
router.register('post', PostViewset, basename='post')

urlpatterns = router.urls
