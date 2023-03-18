"""Sample User models to use in the development environment.

These were intially designed to be used by the `script.reset_database` module."""

from models import User

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


krisj = User(id=1, pid=710453084, onyen='krisj', first_name="Kris", last_name="Jordan",
             email="kris@cs.unc.edu", pronouns="he / him")

sol_student = User(id=2, pid=100000000, onyen='sol', first_name="Sol",
               last_name="Student", email="sol@unc.edu", pronouns="they / them")

arden_ambassador = User(id=3, pid=100000001, onyen='arden', first_name="Arden",
               last_name="Ambassador", email="arden@unc.edu", pronouns="they / them")

merritt_manager = User(id=4, pid=100000002, onyen='merritt', first_name="Merritt",
               last_name="Manager", email="merritt@unc.edu", pronouns="they / them")

models = [
    krisj,
    sol_student,
    arden_ambassador,
    merritt_manager
]
