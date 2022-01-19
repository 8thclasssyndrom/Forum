from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.models import Fandom, Fanfic, Comment, Like
from main.permissions import IsAuthor
from main.serializers import FandomSerializer, FanficSerializer, FanficListSerializer, CreateRatingSerializer, \
    CommentCreateSerializer, LikeSerializer


class FandomViewSet(ModelViewSet):
    """Просмотр Фандомов и добавление их"""
    queryset = Fandom.objects.all()
    serializer_class = FandomSerializer


class FanficListCreateView(ListCreateAPIView):
    """Список фанфиков"""
    queryset = Fanfic.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FanficListSerializer
        return FanficSerializer


class FanficRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Fanfic.objects.all()
    serializer_class = FanficSerializer


class FanficViewSet(ModelViewSet):
    """Добавление, удаление, создание фанфиков"""
    queryset = Fanfic.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'language', 'content']
    serializer_class = FanficSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return FanficListSerializer
        return FanficSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        # elif self.action == 'comments':
        #     if self.request.method == 'POST':
        #         return [IsAuthenticated()]
        #     return []
        return [IsAdminUser()]


class CommentView(ModelViewSet):
    """Создание комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class UpdateDeleteCommentView(DestroyModelMixin,UpdateModelMixin, GenericAPIView):
    """Изменение, Удаление комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthor]

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RatingView(CreateAPIView):
    """Добавление рейтинга"""
    serializer_class = CreateRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}



class LikeView(ModelViewSet):
    """Добавление лайков"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}

