from typing import Any, Generic, TypeVar
from uuid import UUID

from django.db import models
from django.db.models import QuerySet


ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def exists_by_id(self, entity_id: UUID) -> bool:
        return self.model.objects.filter(id=entity_id).exists()

    def get_by_id(self, entity_id: UUID) -> ModelType:
        return self.model.objects.get(id=entity_id)

    def get_all(self) -> QuerySet[ModelType]:
        return self.model.objects.all()

    def filter(self, **filters: Any) -> QuerySet[ModelType]:
        return self.model.objects.filter(**filters)

    def create(self, **data: Any) -> ModelType:
        return self.model.objects.create(**data)

    def update(
        self,
        entity: ModelType,
        **data: Any,
    ) -> ModelType:
        for field, value in data.items():
            setattr(entity, field, value)

        entity.save()

        return entity

    def delete(self, entity: ModelType) -> None:
        entity.delete()

    def delete_all(self, **filters: Any) -> int:
        deleted_count, _ = self.model.objects.filter(**filters).delete()

        return deleted_count