from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_homepage, name='musi-homepage'),
    path('bands/', views.BandList.as_view(), name='band-list'),
    path('bands/<int:pk>/', views.BandDetail.as_view(), name='band-detail'),
    path('albums/', views.AlbumList.as_view(), name='album-list'),
    path('albums/<int:pk>/', views.AlbumDetail.as_view(), name='album-detail'),
    path('songs/', views.SongList.as_view(),name='song-list' ),
    path('songs/<int:pk>/', views.SongDetail.as_view(), name='song-detail'),
    path('reviews/', views.AlbumReviewList.as_view(), name='album-review-list'),
    path('reviews/<int:pk>/', views.AlbumReviewDetail.as_view(), name='album-review-detail'),
    path('comments/', views.AlbumReviewCommentList.as_view(), name='album-review-comment-list'),
    path('comments/<int:pk>/delete/', views.AlbumReviewCommentDetail.as_view(), name='album-review-comment-detail'),
    path('<int:album_review_id>/like/', views.AlbumReviewLikeCreate.as_view(), name='album-review-like-create'),
    # path('likes/', views.AlbumReviewLikeList.as_view()),
    # path('likes/<int:pk>/', views.AlbumReviewLikeDetail.as_view()),
]