from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models, serializers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse_lazy


@api_view(['GET'])
def music_homepage(request):
    return Response({
        'bands': reverse_lazy('band-list'),
        'songs': reverse_lazy('song-list'),
        'albums': reverse_lazy('album-list'),
        'reviews': reverse_lazy('album-review-list'),
        'comments': reverse_lazy('album-review-comment-list'),
    })


class UserOwnedObjectRUDMixin():
    def delete(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))

    def put(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))


class BandList(generics.ListCreateAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer


class BandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer


class AlbumList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save()


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class SongList(generics.ListCreateAPIView):
    serializer_class = serializers.SongSerializer
    queryset = models.Song.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save()

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(song_id=self.kwargs['song_id'])
    #     return qs


class SongDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.SongSerializer
    queryset = models.Song.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    
class AlbumReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumReviewSerializer
    queryset = models.AlbumReview.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(album_id=self.kwargs['album_id'])
    #     return qs


class AlbumReviewDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.AlbumReviewSerializer
    queryset = models.AlbumReview.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AlbumReviewCommentList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumReviewCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.AlbumReviewComment.objects.all()

    # def get_queryset(self):
    #     review_id = self.kwargs['review_id']
    #     return models.AlbumReviewComment.objects.filter(album_review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        album_review = get_object_or_404(models.AlbumReview, pk=review_id)
        serializer.save(user=self.request.user, album_review=album_review)


class AlbumReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.AlbumReviewCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        album_review = get_object_or_404(models.AlbumReview, pk=self.kwargs.get('album_review'))
        return get_object_or_404(models.AlbumReviewComment, pk=self.kwargs.get('pk'), album_review=album_review)
        

class AlbumReviewLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.AlbumReviewLikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return models.AlbumReviewLike.objects.filter(
            user=self.request.user, 
            album_review=models.AlbumReview.objects.get(id=self.kwargs['album_review_id'])
        )
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You already like this.'))
        else:
            serializer.save(
                user=self.request.user, 
                album_review=models.AlbumReview.objects.get(id=self.kwargs['album_review_id'])
            )

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_('You cannot unlike what you don\'t like.'))
