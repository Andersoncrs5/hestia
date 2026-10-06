from uuid import UUID

from src.shared.repositories import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def exists_by_email(self, email: str) -> bool:
        return self.model.objects.filter(
            email=email,
        ).exists()

    def get_by_email(self, email: str) -> User:
        return self.model.objects.get(
            email=email,
        )

    def get_by_permission(
        self,
        permission_slug: str,
    ) -> list[User]:
        return list(
            self.model.objects.filter(
                permissions__slug=permission_slug,
                permissions__is_active=True,
            ).distinct()
        )

    def has_permission(
        self,
        user_id: UUID,
        permission_slug: str,
    ) -> bool:
        return self.model.objects.filter(
            id=user_id,
            permissions__slug=permission_slug,
            permissions__is_active=True,
        ).exists()