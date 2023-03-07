from rest_framework import serializers
from . import models


class BandSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = models.Band
        fields = ('id', 'name')


class SongSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    duration = serializers.IntegerField()

    class Meta:
        model = models.Song
        fields = ('id', 'name', 'duration')


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    band = BandSerializer(read_only=True)
    songs = SongSerializer(many=True)

    class Meta:
        model = models.Album
        fields = ('id', 'name', 'band', 'songs')


class AlbumReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    album = serializers.PrimaryKeyRelatedField(queryset=models.Album.objects.all())
    album_name = serializers.CharField(source='album.name', read_only=True)
    album_band = serializers.CharField(source='album.band.name', read_only=True)

    class Meta:
        model = models.AlbumReview
        fields = ('id', 'user', 'album', 'album_name', 'album_band', 'content', 'score')


class AlbumReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    album_review = serializers.PrimaryKeyRelatedField(queryset=models.AlbumReview.objects.all())
    album_review_id = serializers.IntegerField(source='album_review.id', read_only=True)

    class Meta:
        model = models.AlbumReviewComment
        fields = ('id', 'user', 'album_review', 'album_review_id', 'content')


class AlbumReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    album_review = serializers.PrimaryKeyRelatedField(queryset=models.AlbumReview.objects.all())

    class Meta:
        model = models.AlbumReviewLike
        fields = ('id', 'user', 'album_review')