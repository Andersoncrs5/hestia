from django.db import models

from src.shared.models import BaseModel


class RoomType(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    capacity = models.PositiveIntegerField()

    class Meta:
        db_table = "room_types"
        ordering = ["name"]

    def __str__(self):
        return self.name