"""
Verify connectivity to the database from the service layer for health check purposes.

The production system will regularly check the health of running containers via accessing an API endpoint.
The API endpoint is backed by this service which executes a simple statement against our backing database.
In more complex deployments, where multiple backing services may be depended upon, the health check process
would necessarily also become more complex to reflect the health of all subsystems.

In this context health does not refer to correctness as much as running, connected, and responsive.
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy import text
from ..models.openai_test_response import OpenAITestResponse
from ..database import Session, db_session
from ..services.openai import OpenAIService

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class HealthService:
    _session: Session
    _openai_svc: OpenAIService

    def __init__(
        self,
        session: Annotated[Session, Depends(db_session)],
        openai_svc: Annotated[OpenAIService, Depends()],
    ):
        self._session = session
        self._openai_svc = openai_svc

    def check(self):
        stmt = text("SELECT 'OK', NOW()")
        result = self._session.execute(stmt)
        row = result.all()[0]
        return str(f"{row[0]} @ {row[1]}")

    def check_openai(self) -> OpenAITestResponse:
        # Placeholder for OpenAI health check
        system_prompt = "You are a student at UNC-Chapel Hill."
        user_prompt = "Who is our most famous basketball player?"
        response_model = OpenAITestResponse
        return self._openai_svc.prompt(system_prompt, user_prompt, response_model)
