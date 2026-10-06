from src.permissions.models import Permission
from src.permissionsUser.models import PermissionUser
from src.shared.repositories import BaseRepository, ModelType
from src.users.models import User


class PermissionUserRepository(BaseRepository[PermissionUser]):
    def __init__(self):
        super().__init__(PermissionUser)

    def exists_by_user_and_permission(self, user: User, permission: Permission):
        return PermissionUser.objects.filter(user=user, permission=permission).exists()