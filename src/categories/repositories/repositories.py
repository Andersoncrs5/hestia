from src.categories.models import Category
from src.shared.repositories import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)