from rest_framework.decorators import api_view
from rest_framework import generics, reverse
from rest_framework.response import Response
from oscar.apps.catalogue import models
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView

from . import serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse.reverse('product-list', request=request)
    })


class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        product = models.Product.objects.all()
        #product = product.objects.filter(user=self.request.GET['user'])
        return product


class ProductDetail(generics.ListCreateAPIView):
    model = models.Product
    serializer_class = serializers.ProductSerializer


class ProductClassList(generics.ListAPIView):
    model = models.ProductClass


class ProductClassDetail(generics.RetrieveAPIView):
    model = models.ProductClass


class UserList(generics.ListCreateAPIView):
    from django.contrib.auth.models import User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    model = User

class UserDetail(generics.RetrieveAPIView):
    from django.contrib.auth.models import User
    queryset = User.objects.all()
    model = User
    #renderer_classes = (JSONRenderer,)

class FriendshipList(generics.ListAPIView):
    from apps.friendship.models import FriendShip
    serializer_class = serializers.FriendShipListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    #renderer_classes = (JSONRenderer,)
    model = FriendShip

    def get_queryset(self):
        from apps.friendship.models import FriendShip
        return FriendShip.get_friend_list(self.request.user)

class FriendRequest(generics.CreateAPIView):
    from apps.friendship.models import FriendShip
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    model = FriendShip


