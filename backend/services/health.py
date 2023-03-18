"""Verify connectivity to the database from the service layer for health check purposes.

The production system will regularly check the health of running containers via accessing an API endpoint.
The API endpoint is backed by this service which executes a simple statement against our backing database.
In more complex deployments, where multiple backing services may be depended upon, the health check process
would necessarily also become more complex to reflect the health of all subsystems.

In this context health does not refer to correctness as much as running, connected, and responsive.
"""

from fastapi import Depends
from sqlalchemy import text
from ..database import Session, db_session

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class HealthService:
    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def check(self):
        stmt = text("SELECT 'OK', NOW()")
        result = self._session.execute(stmt)
        row = result.all()[0]
        return str(f"{row[0]} @ {row[1]}")
