from django.conf import settings
from django.db import models

from src.rooms.models import Room
from src.shared.models import BaseModel


class ReservationStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    CANCELLED = "cancelled", "Cancelled"
    COMPLETED = "completed", "Completed"


class Reservation(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.SCHEDULED,
    )

    class Meta:
        db_table = "reservations"
        ordering = ["starts_at"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    ends_at__gt=models.F("starts_at"),
                ),
                name="reservation_valid_period",
            ),
        ]

    def __str__(self):
        return f"{self.room} - {self.starts_at}"