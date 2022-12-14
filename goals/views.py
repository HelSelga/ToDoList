from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, Status, GoalComment
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalSerializer, GoalCommentCreateSerializer, \
    GoalCommentListSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]

    search_fields = ["title"]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", "description"]
    filterset_class = GoalDateFilter

    ordering_fields = ["title", "created"]
    ordering = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user, is_deleted=False)
        # return Goal.objects.select_related("category__board", "user").filter(
        #     category__board__participants__user=self.request.user, is_deleted=False
        # )


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user, is_deleted=False)
        # return Goal.objects.select_related("category__board", "user").filter(
        #     category__board__participants__user=self.request.user, is_deleted=False
        # )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["goal"]

    ordering_fields = ["created"]
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user, is_deleted=False)
        # return GoalComment.objects.select_related("goal__category__board", "user").filter(
        #     goal__category__board__participants__user_id=self.request.user.id
        # )


class GoalCommentDetailView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user, is_deleted=False)
        # return GoalComment.objects.select_related("goal__category__board", "user").filter(
        #     goal__category__board__participants__user_id=self.request.user.id
        # )


# class BoardView(RetrieveUpdateDestroyAPIView):
#     model = Board
#     permission_classes = [IsAuthenticated, BoardPermissions]
#     serializer_class = BoardSerializer
#
#     def get_queryset(self):
#         return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
#
#     def perform_destroy(self, instance: Board):
#         with transaction.atomic():
#             instance.is_deleted = True
#             instance.save()
#             instance.categories.update(is_deleted=True)
#             Goal.objects.filter(category__board=instance).update(
#                 status=Goal.Status.archived
#             )
#         return instance


# class BoardDetailView(RetrieveUpdateDestroyAPIView):
#     model = Board
#     serializer_class = BoardListSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = LimitOffsetPagination
#
#     ordering_fields = ["title"]
#     ordering = ["title"]
#
#     def get_queryset(self):
#         return Board.objects.filter(user=self.request.user, is_deleted=False)
