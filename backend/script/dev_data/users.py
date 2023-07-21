"""Sample User models to use in the development environment.

These were intially designed to be used by the `script.reset_database` module."""

from backend.entities.user_entity import UserEntity

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


root = UserEntity(id=1, pid=999999999, onyen='root', first_name="Super", last_name="User",
             email="root@cs.unc.edu", pronouns="they / them")

sol_student = UserEntity(id=2, pid=100000000, onyen='sol', first_name="Sol",
               last_name="Student", email="sol@unc.edu", pronouns="they / them")

arden_ambassador = UserEntity(id=3, pid=100000001, onyen='arden', first_name="Arden",
               last_name="Ambassador", email="arden@unc.edu", pronouns="they / them")

merritt_manager = UserEntity(id=4, pid=100000002, onyen='merritt', first_name="Merritt",
               last_name="Manager", email="merritt@unc.edu", pronouns="they / them")

models = [
    root,
    sol_student,
    arden_ambassador,
    merritt_manager
]
