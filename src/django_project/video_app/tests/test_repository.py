import pytest

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.django_project.video_app.models import Video as VideoORM
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.mark.django_db
class TestSave:
    def test_saves_video_in_database(self):
        video = Video(
            title="Batman - The Dark Knight",
            description="Batman, Lieutenant James Gordon, and District Attorney Harvey Dent are working to keep Gotham City safe from crime, but the Joker, a mysterious criminal mastermind, appears and throws the city into chaos",
            launch_year=2008,
            opened=True,
            duration=152.0,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository = DjangoORMVideoRepository()

        assert VideoORM.objects.count() == 0
        repository.save(video)
        assert VideoORM.objects.count() == 1
        saved_video = VideoORM.objects.get()

        assert saved_video.id == video.id
