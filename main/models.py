from django.conf import settings
from django.db import models
from model_utils import Choices


LANGUAGE = Choices('English', 'Russian', 'Espanol', 'Chinese', 'French')
RATING = Choices('1', '2', '3', '4', '5')


class Fandom(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Fanfic(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fanfics')
    language = models.CharField(choices=LANGUAGE, max_length=20)
    image = models.ImageField(upload_to='fanfics', default='default.png')
    content = models.TextField(default='Текст еще не был добавлен(')
    fandom = models.ForeignKey(Fandom,
                               on_delete=models.CASCADE,
                               related_name='fanfics')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    fanfic = models.ForeignKey(Fanfic, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rating')
    star = models.CharField(choices=RATING, max_length=100)
    fanfic = models.ForeignKey(Fanfic, on_delete=models.CASCADE, related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.fanfic}"

    class Meta:
        ordering = ["-star"]


class Like(models.Model):
    likes = models.BooleanField(default=False)
    fanfic = models.ForeignKey(Fanfic, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')


class Favorite(models.Model):
    fanfic = models.ForeignKey(Fanfic, on_delete=models.CASCADE, related_name='favorities')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)

