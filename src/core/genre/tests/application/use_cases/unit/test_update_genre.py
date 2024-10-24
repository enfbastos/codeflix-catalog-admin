from unittest.mock import create_autospec
import uuid

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestUpdateCategory:
    def test_when_genre_does_not_exist_then_raise_error(
        self, 
        mock_empty_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository
    ):  
        mock_genre_repository.get_by_id.return_value = None
        
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository, 
            category_repository=mock_empty_category_repository
        )
        
        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Genre 1",
            is_active=True,
            categories=set()
        )
        
        with pytest.raises(GenreNotFound, match="Genre with .* not found") as exc:
            use_case.execute(input)
            
        mock_genre_repository.update.assert_not_called()
    
    @pytest.mark.parametrize(
        "payload",
        [
            {
                "name": "",
                "is_active": True,
                "categories": set()
            },
            {
                "name": "#"*256,
                "is_active": True,
                "categories": set()
            }
        ],
    )
    def test_when_updated_genre_is_invalid_then_raise_invalid_genre(
        self,
        payload: dict,
        mock_empty_category_repository: CategoryRepository,
        mock_genre_repository: CategoryRepository
    ):
        genre_id = uuid.uuid4()
        genre = Genre(id=genre_id, name="Drama")
        mock_genre_repository.get_by_id.return_value = genre
        
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )
        
        input = UpdateGenre.Input(
            id=genre_id,
            **payload
        )
        
        with pytest.raises(InvalidGenre) as exc:
            use_case.execute(input)
        
        mock_genre_repository.update.assert_not_called()
        
    def test_when_provided_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_empty_category_repository: CategoryRepository,
        mock_genre_repository: CategoryRepository
    ):
        category_id = uuid.uuid4()

        genre_id = uuid.uuid4()
        genre = Genre(id=genre_id, name="Drama")
        mock_genre_repository.get_by_id.return_value = genre
        
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )
        
        input = UpdateGenre.Input(
            id=genre_id,
            name="Drama",
            is_active=True,
            categories={category_id}
        )
        
        with pytest.raises(RelatedCategoriesNotFound, match="Categories with provided IDs not found: ") as exc:
            use_case.execute(input)
            
        assert str(category_id) in str(exc.value)
        
    def test_when_updated_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        movie_category: Category,
        documentary_category: Category,
        mock_category_repository_with_categories: CategoryRepository,
        mock_genre_repository: CategoryRepository  
    ):  
        genre_id = uuid.uuid4()
        genre = Genre(id=genre_id, name="Drama", is_active=True, categories={movie_category.id, documentary_category.id})
        mock_genre_repository.get_by_id.return_value = genre
    
        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        
        input = UpdateGenre.Input(
            id=genre_id,
            name="Comedia",
            is_active=False,
            categories={movie_category.id}
        )
        
        use_case.execute(input)
        
        mock_genre_repository.update.assert_called_once_with(
            Genre(
                id=genre_id,
                name="Comedia",
                is_active=False,
                categories={movie_category.id}
            )
        )
