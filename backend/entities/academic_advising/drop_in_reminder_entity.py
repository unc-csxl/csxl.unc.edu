"""Definition of SQLAlchemy table-backed object mapping entity for Advising Drop-in Reminders."""

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from datetime import datetime
from ...models.public_user import PublicUser
from ...models.academic_advising import DropInReminder

__author__ = "Emmalyn Foster"
__copyright__ = "Copyright 2024"
__license__ = "MIT"

class DropInReminderEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `DropInReminders` table

    This table is the association / join table to establish the many-to-many relationship
    between the `user` and `drop-in` tables. This allows many users to register for one event, and
    users be registered for many events.

    To establish this relationship, this entity contains two primary key fields for each related
    table.
    """

    # Name for the events table in the PostgreSQL database
    __tablename__ = "drop_in_reminder"

      # Event for the current drop in session
    # NOTE: This is ultimately a join table for a many-to-many relationship
    drop_in_id: Mapped[int] = mapped_column(ForeignKey("drop_in.id"), primary_key=True)
    drop_in: Mapped["DropInEntity"] = relationship(back_populates="drop_in_reminders")

    # User for the current drop in session
    # NOTE: This is ultimately a join table for a many-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["UserEntity"] = relationship()


    @classmethod
    def from_new_model(cls, model: DropInReminder) -> Self:
      """
      Class method that converts an `NewDropInReminder` model into a `DropInReminderEntity`

        Parameters:
          - model (DropInReminder): Model to convert into an entity
        Returns:
          DropInReminderEntity: Entity created from model
      """
      return cls(
        drop_in_id=model.drop_in_id,
        user_id=model.user_id,
      )

    @classmethod
    def to_model(self) -> DropInReminder:
      """
      Converts an `DropInReminderEntity` into an `DropInReminder` model object
      to store reminder information.

      Returns:
        DropInReminder: `DropInReminder` object from the entity
      """
      return DropInReminder(
        drop_in_id = self.drop_in_id,
        user_id = self.user_id,
        drop_in = self.drop_in.to_model(),
        user=self.user.to_model(),
      )

