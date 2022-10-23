from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from goals.models import BoardParticipant, GoalCategory, Goal


class BoardPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryCreatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        board_id = request.data.get("board")
        board = get_object_or_404(Board, pk=board_id)
        return BoardParticipant.objects.filter(
            user=request.user,
            board=board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCategoryDetailPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        category_id = request.data.get("category")
        category = get_object_or_404(GoalCategory, pk=category_id)

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=category.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user,
            board=category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalDetailPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCommentCreatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        goal_id = request.data.get("goal")
        goal = get_object_or_404(Goal, pk=goal_id)
        return BoardParticipant.objects.filter(
            user=request.user,
            board=goal.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCommentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.goal.category.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()
