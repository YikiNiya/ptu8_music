from django.contrib import admin
from . import models


admin.site.register(models.Band)
admin.site.register(models.Album)
admin.site.register(models.Song)
admin.site.register(models.AlbumReview)
admin.site.register(models.AlbumReviewComment)
admin.site.register(models.AlbumReviewLike)