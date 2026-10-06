from src.room_types.models import RoomType
from src.shared.repositories import BaseRepository


class RoomTypeRepository(BaseRepository[RoomType]):
    def __init__(self):
        super().__init__(RoomType)

    def exists_by_name(self, name: str) -> bool:
        return RoomType.objects.filter(name=name).exists()