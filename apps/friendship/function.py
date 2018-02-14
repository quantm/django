#__author__ = 'Tam'
from .models import *

# Check Already Requested From Other
def is_ready_requested(user_self,user_obj):
    ready = FriendShip.objects.filter(user_self=user_obj, user_obj=user_self, type=Message_Type._FRIEND_REQUEST)
    if len(ready) > 0:
        return True
    return False

# Check Already Requested From this User
def is_requested(user_self,user_obj):
    ready = FriendShip.objects.filter(user_self=user_self, user_obj=user_obj, type=Message_Type._FRIEND_REQUEST)
    if len(ready) > 0:
        return True
    return False

def is_friend(user_self,user_obj):
    ready_requested = is_ready_requested(user_self,user_obj)
    requested = is_requested(user_self,user_obj)
    dict = {
        'ready_requested': ready_requested,
        'requested': requested,
        'is_friend': False
    }
    if ready_requested and requested:
        dict['is_friend'] = True

    return dict

def is_follower(user_self,user_obj):
    ready = FriendShip.objects.filter(user_self=user_self, user_obj=user_obj, type=Message_Type._REQUEST_FOLLOWER)
    if len(ready) > 0:
        return True
    return False


