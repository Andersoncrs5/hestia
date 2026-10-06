from src.rooms.models import Room
from src.shared.repositories import BaseRepository


class RoomRepository(BaseRepository[Room]):
    def __init__(self) -> None:
        super().__init__(Room)

    def exists_by_name(self, name: str) -> bool:
        return Room.objects.filter(name=name).exists()