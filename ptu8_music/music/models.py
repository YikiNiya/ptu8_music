from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Band(models.Model):
    name = models.CharField(max_length=150)

    
class Album(models.Model):
    name = models.CharField(max_length=200)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='albums')


class Song(models.Model):
    name = models.CharField(max_length=100)
    duration = models.FloatField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')


def duration_as_str(self):
    minutes, seconds = divmod(self.duration.total_seconds(), 60)
    return f'{int(minutes)}:{int(seconds):02d}'


class AlbumReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_reviews')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_reviews')
    content = models.CharField(max_length=200)
    score = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}, {self.content[:100]}'


class AlbumReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_review_comments')
    album_review = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='album_review_comments') 
    content = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.id}, {self.content[:100]}'


class AlbumReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_review_likes')
    album_review = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='album_review_likes')