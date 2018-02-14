from django.db import models
from django.contrib.auth.models import User
from apps.common.models import Message_Type


class FriendShip(models.Model):
    user_self = models.ForeignKey(User, related_name='user_self')
    user_obj = models.ForeignKey(User, related_name='user_obj')
    type = models.IntegerField(max_length=32, blank=True, null=True)

    @staticmethod
    def get_friend_list(user):
        friends = FriendShip.objects.filter(user_obj=user, type=Message_Type._FRIEND_REQUEST)
        return friends
    def to_json(self):
        dict = {
                    'id':self.user_obj.id,
                    'email':self.user_obj.email,
                    'is_active': self.user_obj.is_active,
                    'full_name':self.user_obj.get_full_name(),
                    'is_staff': self.user_obj.is_staff,
                    'last_login':self.user_obj.last_login,
                    'date_joined':self.user_obj.date_joined,
                }
        return (dict)

    class Meta:
        unique_together = ('user_self', 'user_obj', 'type')
        db_table = u'friendship'