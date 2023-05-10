from rest_framework import generics, permissions

from todolist.goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryPermission(permissions.IsAuthenticated):

    def has_object_permission(self, view: generics.GenericAPIView, obj: GoalCategory) -> bool:
        return request.user == obj.user


class GoalPermission(permissions.IsAuthenticated):

    def has_object_permission(self, view: generics.GenericAPIView, obj: Goal) -> bool:
        return request.user == obj.user


class GoalCommentPermission(permissions.IsAuthenticated):

    def has_object_permission(self, view: generics.GenericAPIView, obj: GoalComment) -> bool:
        return request.user == obj.user