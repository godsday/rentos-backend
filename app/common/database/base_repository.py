# from typing import Generic, TypeVar

# from sqlalchemy.orm import Session

# from app.db.base import BaseEntity

# ModelType = TypeVar("ModelType", bound=BaseEntity)


# class BaseRepository(Generic[ModelType]):
#     def __init__(self, db: Session, model: type[ModelType]):
#         self.db = db
#         self.model = model

#     def create(self, entity: ModelType) -> ModelType:
#         self.db.add(entity)
#         self.db.commit()
#         self.db.refresh(entity)
#         return entity

#     def get_by_id(self, entity_id):
#         return (
#             self.db.query(self.model)
#             .filter(
#                 self.model.id == entity_id,
#                 self.model.is_deleted.is_(False),
#             )
#             .first()
#         )

#     def get_all(self):
#         return (
#             self.db.query(self.model)
#             .filter(self.model.is_deleted.is_(False))
#             .all()
#         )

#     def update(self, entity: ModelType) -> ModelType:
#         self.db.commit()
#         self.db.refresh(entity)
#         return entity

#     def soft_delete(self, entity: ModelType):
#         entity.is_deleted = True
#         self.db.commit()

#     def hard_delete(self, entity: ModelType):
#         self.db.delete(entity)
#         self.db.commit()