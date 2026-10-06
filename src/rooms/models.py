from django.db import models

from src.categories.models import Category
from src.room_types.models import RoomType
from src.shared.models import BaseModel


class Room(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name="rooms",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="rooms",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "rooms"
        ordering = ["name"]

    def __str__(self):
        return self.name