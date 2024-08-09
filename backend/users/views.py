from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import (ListSubscriptionsSerialaizer,
                                       SubscriptionsGetSerializer)
from users.serializers import UserAvatarSerializer, UserCustomSerializer
from utils.pagination import PageLimitPagination

User = get_user_model()


class CustomUsersViewSet(viewsets.GenericViewSet):
    """ViewSet для управление пользователями."""

    queryset = User.objects.all()
    serializer_class = UserCustomSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def me(self, request):
        serializer = UserCustomSerializer(
            request.user, context={"request": request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['PUT', 'DELETE'],
        permission_classes=(IsAuthenticated,),
        url_path='me/avatar',
        serializer_class=UserAvatarSerializer,
    )
    def avatar(self, request):
        if request.method == 'PUT':
            if request.data:
                serializer = self.get_serializer(
                    request.user,
                    data=request.data,
                    partial=True,
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            self.request.user.avatar.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,),
        serializer_class=ListSubscriptionsSerialaizer,
        pagination_class=PageLimitPagination,
    )
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        subscribe = Subscription.objects.filter(
            user=user.id, author=author.id
        )
        if request.method == 'POST':
            serializer = ListSubscriptionsSerialaizer(
                data={
                    'user': user.id,
                    'author': author.id,
                },
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
        pagination_class=PageLimitPagination,
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsGetSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
