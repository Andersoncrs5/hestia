from django.db import models

from src.permissions.models import Permission
from src.shared.models import BaseModel
from src.users.models import User


class PermissionUser(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="permission_users",
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        db_column="permission_id",
        related_name="permission_users",
    )

    class Meta:
        db_table = "permission_user"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "permission"],
                name="uq_permission_user",
            ),
        ]