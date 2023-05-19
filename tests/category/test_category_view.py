import pytest


@pytest.mark.django_db
def test_get_category_list_not_authorized(client) -> None:
    """
    Неавторизованный пользователь не может просматривать категории
    """
    response = client.get("/goals/goal_category/list")

    assert response.status_code == 403
    assert response.json() == {"detail": "Учетные данные не были предоставлены."}


def test_create_category(client, create_category) -> None:
    """
    Неавторизованный пользователь не может создать категорию
    """
    response = create_category

    created = response.json()
    assert response.status_code == 201
    assert created == {
        "title": "Test_Category",
        "id": created.get("id"),
        "is_deleted": False,
        "created": created.get("created"),
        "updated": created.get("updated"),
        "board": created.get("board"),
    }


def test_get_category_list(client, create_category) -> None:
    """
    Неавторизованный пользователь не может получить список категорий
    """
    response = client.get("/goals/goal_category/list")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert type(response.json()) is list


def test_get_single_category(client, create_category) -> None:
    """
    Неавторизованный пользователь не может получить категорию
    """
    category_data = create_category.data
    pk = category_data.get("id")
    response = client.get(f"/goals/goal_category/{pk}")

    received = response.json()
    received.pop("user")
    assert response.status_code == 200
    assert type(received) is dict
    assert received == category_data


def test_delete_category(client, create_category) -> None:
    """
    Неавторизованный пользователь не может удалить категорию
    """
    category_data = create_category.data
    pk = category_data.get("id")

    response = client.delete(f"/goals/goal_category/{pk}")

    assert response.status_code == 204

    new_response = client.get(f"/goals/goal_category/{pk}")

    assert new_response.status_code == 404