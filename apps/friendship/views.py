# Create your views here.
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import HttpResponse
import json
from apps.common.functions import Message_Type, send_message
from .function import *

def request_friend(request):
    #check current user is logged in
    current_user = request.user
    try:
        user_obj_id = request.POST['uid']
        action = request.POST['action']
        if current_user.id:
            req = False
            if action == "make_friend":
                req = _request_friend(user_self_id=current_user.id,user_obj_id=user_obj_id, subject='Request friend from '+ current_user.get_full_name())
            if action == "accept_request":
                req = _response_friend(user_self_id=current_user.id,user_obj_id=user_obj_id, subject=current_user.get_full_name() + ' accept friend with you')
            if action == "unfriend_request":
                req = _unfriend(user_self_id=current_user.id,user_obj_id=user_obj_id)
            if action == "delete_request":
                req = _delete_request(user_self_id=current_user.id,user_obj_id=user_obj_id)
            if action == "make_follow":
                req = _request_follow(user_self_id=current_user.id,user_obj_id=user_obj_id)
            if action == "unfollow":
                req = _request_unfollow(user_self_id=current_user.id,user_obj_id=user_obj_id)

            if req:
                return HttpResponse(json.dumps({'error':''}))
            else:
                return HttpResponse(json.dumps({'error':'12'}))
        else:
            return HttpResponse(json.dumps({'error':'13'}))
    except Exception, ex:
        return HttpResponse(json.dumps({'error':'11'}))

def _request_friend(user_self_id, user_obj_id, subject="Request friend"):
    if int(user_self_id) == int(user_obj_id):
        return False

    friend = is_friend(user_self_id, user_obj_id)
    try:
        if friend['is_friend'] or friend['ready_requested'] or friend['requested']:
            return False
        else:
            friendship = FriendShip(user_self_id=user_self_id,user_obj_id=user_obj_id,type=Message_Type._FRIEND_REQUEST)
            friendship.save()
            send_message(recipient_id=user_obj_id,sender_id=user_self_id,subject=subject,type=Message_Type._FRIEND_REQUEST)
    except Exception, ex:
        return False
    return True

def _response_friend(user_self_id, user_obj_id, subject="Request friend"):
    if int(user_self_id) == int(user_obj_id):
        return False

    friend = is_friend(user_self_id, user_obj_id)
    try:
        if friend['is_friend'] or friend['requested']:
            return False
        if friend['ready_requested']:
            friendship = FriendShip(user_self_id=user_self_id,user_obj_id=user_obj_id,type=Message_Type._FRIEND_REQUEST)
            friendship.save()
            send_message(recipient_id=user_obj_id,sender_id=user_self_id,subject=subject,type=Message_Type._FRIEND_REQUEST)
    except Exception, ex:
        return False
    return True

def _unfriend(user_self_id, user_obj_id):
    if int(user_self_id) == int(user_obj_id):
        return False
    try:
        FriendShip.objects.filter(user_self_id=user_self_id, user_obj_id=user_obj_id, type=Message_Type._FRIEND_REQUEST).delete()
        FriendShip.objects.filter(user_self_id=user_obj_id, user_obj_id=user_self_id,type=Message_Type._FRIEND_REQUEST).delete()
    except Exception, ex:
        return False

    return True

def _delete_request(user_self_id, user_obj_id):
    if int(user_self_id) == int(user_obj_id):
        return False
    friend = is_friend(user_self_id, user_obj_id)
    try:
        if friend['is_friend'] or friend['requested']:
            return False
        if friend['ready_requested']:
            FriendShip.objects.filter(user_self_id=user_obj_id, user_obj_id=user_self_id, type=Message_Type._FRIEND_REQUEST).delete()
    except Exception, ex:
        return False

    return True

def _request_follow(user_self_id, user_obj_id):
    if int(user_self_id) == int(user_obj_id):
        return False

    ready = is_follower(user_self_id, user_obj_id)

    try:
        if ready :
            return False
        else:
            FriendShip(user_self_id=user_self_id,user_obj_id=user_obj_id,type=Message_Type._REQUEST_FOLLOWER).save()

    except Exception, ex:
        return False

    return True

def _request_unfollow(user_self_id, user_obj_id):
    if int(user_self_id) == int(user_obj_id):
        return False

    ready = is_follower(user_self_id, user_obj_id)

    try:
        if ready :
            FriendShip.objects.filter(user_self_id=user_self_id, user_obj_id=user_obj_id, type=Message_Type._REQUEST_FOLLOWER).delete()

    except Exception, ex:
        return False

    return True