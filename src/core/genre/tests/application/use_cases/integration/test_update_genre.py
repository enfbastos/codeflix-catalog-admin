from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:
    def test_update_genre_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")
        series_category = Category(name="Series")

        category_repository.save(movie_category)
        category_repository.save(documentary_category)
        category_repository.save(series_category)
        
        genre = Genre(name="Drama", categories={movie_category.id, documentary_category.id})
        genre_repository.save(genre)
        
        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        use_case.execute(
            UpdateGenre.Input(
                id=genre.id,
                name="Terror",
                is_active=True,
                categories={series_category.id},
            )
        )

        assert len(genre_repository.list()) == 1
        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == "Terror"
        assert updated_genre.categories == {series_category.id}
        assert updated_genre.is_active is True
