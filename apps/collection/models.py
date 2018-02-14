from django.db import models
from apps.catalogue.models import Product
from django.contrib.auth.admin import User

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('l', 'MyLists'),
    ('c', 'MyCollection'),
    ('e', 'Deleted'),
)


class CollectionSet(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User)
    thumb = models.CharField(max_length=255, blank=True, null=True, default='')
    create = models.DateTimeField(auto_now_add=True, editable=False)
    view = models.IntegerField(max_length=128, null=True, blank=True, default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        db_table = u'collection_set'


class CollectionSetEdit(models.Model):
    set = models.ForeignKey(CollectionSet)
    editor = models.ForeignKey(User)
    creator_id = models.IntegerField(default=0, null=True, max_length=128)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    is_edited = models.IntegerField(default=0, null=True, max_length=128)

    class Meta:
        db_table = u'collection_set_edit'


class CollectionSetElement(models.Model):
    product = models.ForeignKey(Product)
    set = models.ForeignKey(CollectionSet)
    type = models.CharField(max_length=255, null=False, blank=True)
    style = models.TextField(null=True, blank=True)
    class_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = u'collection_set_element'


class CollectionComment(models.Model):
    set = models.ForeignKey(CollectionSet)
    content = models.CharField(max_length=1024, null=True, blank=True)
    user = models.ForeignKey(User)
    user_comment = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = u'collection_comment'


class CollectionText(models.Model):
    set = models.ForeignKey(CollectionSet)
    type = models.CharField(max_length=255, null=False, blank=True, default="div")
    style = models.CharField(max_length=255, null=True, blank=True)
    class_name = models.CharField(max_length=255, null=True, blank=True)
    ck_editor = models.TextField(null=False, blank=True)

    class Meta:
        db_table = u'collection_text'
