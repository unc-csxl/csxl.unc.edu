"""Sample User models to use in the development environment.

These were intially designed to be used by the `script.reset_database` module."""

from ...models import Role

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

sudoer = Role(id=1, name="Sudoers")

staff = Role(id=2, name="Staff")

ambassador = Role(id=3, name="Ambassador")

models = [
    sudoer,
    staff,
    ambassador
]
