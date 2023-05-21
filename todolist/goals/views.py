from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from todolist.permissions import GoalCommentPermission, BoardPermission, GoalPermission, GoalCategoryPermission

from rest_framework import generics, permissions, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

from todolist.goals.filters import GoalDateFilter
from todolist.goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from todolist.goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentWithUserSerializer, GoalCommentSerializer, BoardSerializer, BoardParticipantSerializer


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def perform_create(self, serializer: BoardSerializer) -> None:
        """Делаем текущего пользователя владельцем доски"""
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    filter_backends = [OrderingFilter]
    ordering = ['title']

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(participants__user_id=self.request.user.id).exclude(is_deleted=True)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardParticipantSerializer

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(participants__user_id=self.request.user.id).exclude(is_deleted=True)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    # filter_backends = [OrderingFilter, SearchFilter]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['goal']
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_fields = ['title']
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_fields = ('title', 'description')

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user,  category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal):

        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer


class GoalCommentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentWithUserSerializer
    # filter_backends = [OrderingFilter]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.select_related('user').filter(user_id=self.request.user.id)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentWithUserSerializer
    queryset = GoalComment.objects.select_related('user')