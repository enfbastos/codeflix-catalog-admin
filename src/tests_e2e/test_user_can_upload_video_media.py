import json
import time
from uuid import uuid4

import pika
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from rest_framework.test import APIClient

from src.django_project import settings
from src.django_project.video_app.models import Video as VideoORM


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }


@pytest.fixture
def api_client(django_db_setup) -> APIClient:
    return APIClient()


@pytest.mark.django_db(transaction=True)
class TestUploadVideoMedia:
    def test_user_can_create_video_with_media(self, api_client: APIClient) -> None:
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
                "title": "Batman2 - The Dark Knight",
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
        
        response = api_client.patch(
            f"/api/videos/{video_id}/",
            data=encode_multipart(
                BOUNDARY,
                {
                    'video_file': SimpleUploadedFile(
                        name="file.mp4", 
                        content=b"file_content", 
                        content_type="video/mp4"
                    )
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == 200
        
        video_model = VideoORM.objects.get(id=video_id)
        assert video_model.video.status == "PENDING"
        
        self.send_message_to_rabbit_mq(video_id)
        
        # time.sleep(1)
        # assert video_model.video.status == "COMPLETED"
        
    def send_message_to_rabbit_mq(self, video_id: str):
        QUEUE = "videos.converted"
        HOST = "localhost"
        PORT = 5672
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=HOST,
                port=PORT,
            ),
        )
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE)

        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video",
            },
            "status": "COMPLETED",
        }
        channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(message))

        print("Sent message")
        connection.close()
    
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
