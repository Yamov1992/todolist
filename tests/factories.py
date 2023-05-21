from typing import Any
import pytest
from core.models import User
from core.models import Board
from django.core.handlers.wsgi import WSGIRequest
import factory
from pytest_factoryboy import register
from django.utils import timezone


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('username')
    password = factory.Faker('password')

    class Meta:
        model = User


    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register
class BoardFactory(DatesFactoryMixin):
    title = factory.Faker('sentense')

    class Meta:
        model = Board


@pytest.mark.django_db
@pytest.fixture
def get_user_data() -> dict[str, str]:

    user_data = {
        "username": "test_username",
        "email": "testemail@test.com",
        "password": "test_password",
        "password_repeat": "test_password",
    }

    return user_data


@pytest.mark.django_db
@pytest.fixture
def updated_user_data(get_authorized_user) -> dict[str, Any]:

    user_data = {
        "id": get_authorized_user.id,
        "username": get_authorized_user.username,
        "first_name": "Ivan",
        "last_name": "Pupkin",
        "email": get_authorized_user.email,
    }

    return user_data


@pytest.mark.django_db
@pytest.fixture
def get_authorized_user(client, django_user_model) -> User:

    user_data = {
        "username": "test_username",
        "email": "testemail@test.com",
        "password": "test_password",
    }

    user = django_user_model.objects.create_user(**user_data)

    client.post("/core/login", data=user_data, content_type="application/json")

    return user


@pytest.mark.django_db
@pytest.fixture
def create_board(client, get_authorized_user) -> WSGIRequest:

    board_data = {
        "title": "Test_Board",
    }

    response = client.post(
        "/goals/board/create", data=board_data, content_type="application/json"
    )

    return response


@pytest.mark.django_db
@pytest.fixture
def create_category(client, create_board) -> WSGIRequest:

    category_data = {
        "title": "Test_Category",
        "board": create_board.data.get("id"),
    }

    response = client.post(
        "/goals/goal_category/create",
        data=category_data,
        content_type="application/json",
    )

    return response


@pytest.mark.django_db
@pytest.fixture
def create_goal(client, create_category) -> WSGIRequest:

    goal_data = {
        "title": "Test_Goal",
        "category": create_category.data.get("id"),
    }

    response = client.post(
        "/goals/goal/create", data=goal_data, content_type="application/json"
    )

    return response


@pytest.mark.django_db
@pytest.fixture
def create_comment(client, create_goal) -> WSGIRequest:

    comment_data = {
        "text": "Test_text",
        "goal": create_goal.data.get("id"),
    }

    response = client.post(
        "/goals/goal_comment/create", data=comment_data,
        content_type="application/json"
    )

    return response