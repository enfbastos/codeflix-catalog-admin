from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.cast_member_app.models import CastMember
from src.django_project.cast_member_app.repository import \
    DjangoORMCastMemberRepository
from src.django_project.category_app.repository import \
    DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )
    

@pytest.fixture
def genre_action(category_movie) -> Genre:
    return Genre(
        name="Action",
        is_active=True,
        categories={category_movie.id},
    )
    

@pytest.fixture
def actor():
    return CastMember(
        name="Christian Bale",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director():
    return CastMember(
        name="Christopher Nolan",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_video(
        self,
        category_movie: Category,
        genre_action: Genre,
        actor: CastMember,
        director: CastMember,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        cast_member_repository.save(actor)
        cast_member_repository.save(director)
        
        url = "/api/videos/"
        data = {
            "title": "Batman - The Dark Knight",
            "description": "Batman, Lieutenant James Gordon, and District Attorney Harvey Dent are working to keep Gotham City safe from crime, but the Joker, a mysterious criminal mastermind, appears and throws the city into chaos",
            "launch_year": 2008,
            "opened": True,
            "duration": 152.0,
            "rating": "L",
            "categories": [str(category_movie.id)],
            "genres": [str(genre_action.id)],
            "cast_members": [str(actor.id), str(director.id)],
        }
        response = APIClient().post(url, data=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        
    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = "/api/videos/"
        data = {
            "title": "",
            "description": "",
            "launch_year": "",
            "opened": "",
            "duration": "",
            "rating": "",
            "categories": [],
            "genres": [],
            "cast_members": [],
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "title": ["This field may not be blank."],
            "description": ["This field may not be blank."],
            "launch_year": ["A valid integer is required."],
            "opened": ["Must be a valid boolean."],
            "duration": ["A valid number is required."],
            "rating": ["\"\" is not a valid choice."],
        }
        
        
    def test_when_related_entities_do_not_exist_then_return_400(self) -> None:
        url = "/api/videos/"
        data = {
            "title": "Batman - The Dark Knight",
            "description": "Batman, Lieutenant James Gordon, and District Attorney Harvey Dent are working to keep Gotham City safe from crime, but the Joker, a mysterious criminal mastermind, appears and throws the city into chaos",
            "launch_year": 2008,
            "opened": True,
            "duration": 152.0,
            "rating": "L",
            "categories": [uuid4()],
            "genres": [uuid4()],
            "cast_members": [uuid4()],
        }
        response = APIClient().post(url, data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid categories" in response.data["error"]
        assert "Invalid genres" in response.data["error"]
        assert "Invalid cast members" in response.data["error"]
    