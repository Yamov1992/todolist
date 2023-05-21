import pytest


@pytest.mark.django_db
def test_signup(client, get_user_data) -> None:
    """
    Пользователь получит ошибку если ввел данные неверно
    """
    user_data = get_user_data

    response = client.post(
        "/core/signup", data=user_data, content_type="application/json"
    )

    result = response.json()
    result.pop("password")

    assert response.status_code == 201
    assert result == {
        "username": user_data.get("username"),
        "first_name": "",
        "last_name": "",
        "email": user_data.get("email"),
    }

def test_login(client, get_authorized_user, get_user_data) -> None:
    """
    Пользователь получит ошибку если введет неправильный логин и пароль
    """
    user_data = {
        "username": get_user_data.get("username"),
        "password": get_user_data.get("password"),
    }

    response = client.post(
        "/core/login", data=user_data, content_type="application/json"
    )
    result = response.json()

    assert response.status_code == 201
    assert result["username"] == get_authorized_user.username

def test_get_profile(client, get_authorized_user) -> None:
    """
    Неавторизированный пользователь не может иметь профиль
    """
    user_data = {
        "id": get_authorized_user.id,
        "username": get_authorized_user.username,
        "first_name": get_authorized_user.first_name,
        "last_name": get_authorized_user.last_name,
        "email": get_authorized_user.email,
    }

    response = client.get("/core/profile")
    result = response.json()

    assert response.status_code == 200
    assert result == user_data

def test_change_profile(client, updated_user_data) -> None:
    """
    неавторизированный пользователь не может изменить профиль
    """
    user_data = updated_user_data

    response = client.put(
        "/core/profile", data=user_data, content_type="application/json"
    )
    result = response.json()

    assert response.status_code == 200
    assert result == user_data

def test_delete_profile(client, get_authorized_user) -> None:
    """
    неавторизированный пользователь не может удалить профиль
    """
    response = client.delete("/core/profile")
    assert response.status_code == 204

    new_response = client.get("/core/profile")
    assert new_response.status_code == 403

def test_update_password(client, get_authorized_user, get_user_data) -> None:
    """
    неавторизированный пользователь не может изменить пароль
    """
    passwords = {
        "old_password": get_user_data.get("password"),
        "new_password": "new_test_password",
    }

    response = client.put(
        "/core/update_password", data=passwords, content_type="application/json"
    )
    result = response.json()
    assert response.status_code == 200
    assert result.get("password") != get_authorized_user.password