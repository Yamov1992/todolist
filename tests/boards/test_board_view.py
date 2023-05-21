import pytest
from django.urls import reverse
from rest_framework import status
from todolist.goals.models import BoardParticipant

@pytest.mark.django_db()
class TestBoardRetrieveView:


    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)


    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь не может просматривать доски
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_board(self, auth_client, board):
        board.is_deleted = True
        board.save()

        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foreign_board(self, client, user_factory):
        another_user = user_factory.create()
        client.forse_login(another_user)

        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestBoardDestroyView:


    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)


    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader
    ], ids=['writer', 'reader'])

    def test_not_owner_failed_to_delete_board(self, client, user_factory, board, board_participant_factory, role):
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_have_to_delete_board(self, auth_client, board):
        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        assert board.is_deleted is True