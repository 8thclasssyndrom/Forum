from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account.views import ProfileView
from main.views import FandomViewSet, FanficViewSet, CommentView, UpdateDeleteCommentView, RatingView, LikeView, \
    FavoriteView

router = DefaultRouter()

router.register('fanfics', FanficViewSet, 'fanfics')
router.register('fandoms', FandomViewSet, 'fandoms')
router.register('comments', CommentView, 'comments')
router.register('like', LikeView, 'like')

urlpatterns = [
    path('', include(router.urls)),
    path('fanfic/favorite/', FavoriteView.as_view()),


]

