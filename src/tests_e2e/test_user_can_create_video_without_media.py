from uuid import uuid4

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateVideoWithoutMedia:
    def test_user_can_create_video_without_media(self, api_client: APIClient) -> None:
        response = api_client.post(
            "/api/categories/",
            {
                "name": "Movie",
                "description": "Movie description",
            },
        )
        assert response.status_code == 201
        category_id = response.data["id"]
        
        response = api_client.post(
            "/api/genres/",
            {
                "name": "Action",
                "is_active": True,
                "categories": {category_id},
            },
        )
        assert response.status_code == 201
        genre_id = response.data["id"]
        
        response = api_client.post(
            "/api/cast_members/",
            {
                "name": "Christian Bale",
                "type": "ACTOR",
            },
        )
        assert response.status_code == 201
        actor_id = response.data["id"]
        
        response = api_client.post(
            "/api/cast_members/",
            {
                "name": "Christopher Nolan",
                "type": "DIRECTOR",
            },
        )
        assert response.status_code == 201
        director_id = response.data["id"]
        
        response = api_client.post(
            "/api/videos/",
            {
                "title": "Batman - The Dark Knight",
                "description": "Batman, Lieutenant James Gordon, and District Attorney Harvey Dent are working to keep Gotham City safe from crime, but the Joker, a mysterious criminal mastermind, appears and throws the city into chaos",
                "launch_year": 2008,
                "opened": True,
                "duration": 152.0,
                "rating": "L",
                "categories": [category_id],
                "genres": [genre_id],
                "cast_members": [actor_id, director_id],
            },
        )
        assert response.status_code == 201
        video_id = response.data["id"]
    
    def test_when_request_data_is_invalid_then_return_400(self, api_client: APIClient) -> None:        
        response = api_client.post(
            "/api/videos/",
            {
                "title": "",
                "description": "",
                "launch_year": "",
                "opened": "",
                "duration": "",
                "rating": "",
                "categories": [],
                "genres": [],
                "cast_members": [],
            },
        )
        assert response.status_code == 400

    def test_when_related_entities_do_not_exist_then_return_400(self, api_client: APIClient) -> None:        
        response = api_client.post(
            "/api/videos/",
            {
                "title": "Batman - The Dark Knight",
                "description": "Batman, Lieutenant James Gordon, and District Attorney Harvey Dent are working to keep Gotham City safe from crime, but the Joker, a mysterious criminal mastermind, appears and throws the city into chaos",
                "launch_year": 2008,
                "opened": True,
                "duration": 152.0,
                "rating": "L",
                "categories": [uuid4()],
                "genres": [uuid4()],
                "cast_members": [uuid4()],
            },
        )
        assert response.status_code == 400
