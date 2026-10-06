from uuid import UUID
from datetime import datetime

from src.reservations.models import Reservation
from src.shared.repositories import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    def __init__(self):
        super().__init__(Reservation)

    def has_conflict(
        self,
        room_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
    ) -> bool:
        return self.model.objects.filter(
            room_id=room_id,
            starts_at__lt=ends_at,
            ends_at__gt=starts_at,
            status="scheduled",
        ).exists()
