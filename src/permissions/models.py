from django.db import models

from src.shared.models import BaseModel


class Permission(BaseModel):
    name = models.CharField(
        max_length=100,
    )

    slug = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "permissions"

    def __str__(self):
        return self.name