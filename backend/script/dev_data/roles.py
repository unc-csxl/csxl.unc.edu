"""Sample User models to use in the development environment.

These were intially designed to be used by the `script.reset_database` module."""

from backend.entities.role_entity import RoleEntity

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

sudoer = RoleEntity(id=1, name="Sudoers")

staff = RoleEntity(id=2, name="Staff")

ambassador = RoleEntity(id=3, name="Ambassador")

models = [
    sudoer,
    staff,
    ambassador
]
