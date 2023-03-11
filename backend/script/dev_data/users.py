"""Sample User models to use in the development environment.

These were intially designed to be used by the `script.reset_database` module."""

from models import User

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


krisj = User(pid=710453084, onyen='krisj', first_name="Kris", last_name="Jordan",
             email="kris@cs.unc.edu", pronouns="he / him")


rameses = User(pid=100000000, onyen='rameses', first_name="Rameses",
               last_name="Sr.", email="ramses@unc.edu", pronouns="they / them")


models = [
    krisj,
    rameses
]
