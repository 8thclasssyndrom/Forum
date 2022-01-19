from rest_framework import serializers
from django.db.models import Avg

from main.models import Fanfic, Fandom, Comment, Rating, Like, Favorite


class FandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fandom
        fields = '__all__'


class FanficListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fanfic
        fields = ['id', 'name', 'user', 'language', 'image', 'content', 'fandom']


class CommentCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Вывод комментариев"""
    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        fanfic = self.context.get('fanfic')
        validated_data['author'] = user
        validated_data['fanfic'] = fanfic
        return super().create(validated_data)


class FanficSerializer(serializers.ModelSerializer):
    """Фанфик"""
    # comments = CommentSerializer(many=True)

    class Meta:
        model = Fanfic
        fields = ['name', 'user', 'language', 'image', 'content', 'fandom']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(),
                                                       many=True).data
        representation['like'] = instance.like.all().count()
        # representation['rating'] = instance.rating.aggregate(Avg('star')).get("star_avg")
        return representation


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "fanfic")

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        fanfic = validated_data.get('fanfic')
        like = Like.objects.get_or_create(user=user, fanfic=fanfic)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['fanfic'] = instance.fanfic.name
        return representation