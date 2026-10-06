from src.permissions.models import Permission
from src.shared.repositories import BaseRepository


class PermissionsRepository(BaseRepository[Permission]):
    def __init__(self):
        super().__init__(Permission)

    def exists_by_slug(self, name: str) -> bool:
        return Permission.objects.filter(name=name).exists()