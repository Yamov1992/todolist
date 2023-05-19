import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def board_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestBoardCreateView:
    url = reverse('todolist.goals:create-board')

    def test_auth_required(self, client, board_create_data):
        """
        Неавторизованный пользователь получит ошибку авторизации при создании доски
        """
        response = client.post(self.url, data=board_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_board(self, auth_client, board_create_data)
        """
        Нельзя создавать удаленную доску
        """
        response = auth_client.post(self.url, data=board_create_data(is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._serialize_board_response(is_deleted=False)

    def test_request_user_bacame_board_owner(self, client, user, board_create_data):
        """
        Пользователь, создавший доску, становится ее владельцем
        """
        response = auth_client.post(self.url, data=board_create_data())

        assert response.status_code == status.HTTP_201_CREATED
        board_participant = BoardParticipant.objects.get(user_id=user_id)
        assert board_participant.board_id == response.data['id']
        assert board_participant.role == BoardParticipant.Role.owner

    def _serialize_board_response(self, **kwargs) -> dict:
        data = {
            'id': ANY,
            'created': ANY,
            'updated': ANY,
            'title': ANY,
            'is_deleted': False
        }
        data |= kwargs
        return data