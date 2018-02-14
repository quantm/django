from django.db import models


class SocialHashTag (models.Model):
    object_id = models.IntegerField(max_length=128, null=True, blank=True, default=0)
    type = models.CharField(max_length=255, null=True, blank=True, default=0)
    hashtag_id = models.IntegerField(max_length=128, null=True, blank=True, default=0)

