"""
This service provides methods to interact with the OpenAI API.

This module encapsulates Azure OpenAI API calls and provides a clean interface
for making AI completion requests using Pydantic models for response parsing.
"""

from ..env import getenv
from typing import Type, TypeVar, Annotated
from fastapi import Depends
from pydantic import BaseModel
from openai import AzureOpenAI

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"

# T is a generic type that will represent a child class of BaseModel.
T = TypeVar("T", bound=BaseModel)

API_KEY = getenv("UNC_OPENAI_API_KEY")
API_VERSION = getenv("UNC_OPENAI_API_VERSION", default="2024-10-21")
API_ENDPOINT = getenv(
    "UNC_OPENAI_API_ENDPOINT", default="https://azureaiapi.cloud.unc.edu"
)


def openai_client():
    """Generator function offering dependency injection of SQLAlchemy Sessions."""
    with AzureOpenAI(
        api_version=API_VERSION,
        azure_endpoint=API_ENDPOINT,
        api_key=API_KEY,
    ) as client:
        yield client


class OpenAIService:
    """Service for interacting with Azure OpenAI API.

    This class provides a simplified interface for making requests to Azure OpenAI API
    and parsing the responses into strongly-typed Pydantic models.

    Attributes:
        _client (AzureOpenAI): The Azure OpenAI client instance.
        _model (str): The model name to use for completions.
    """

    _client: AzureOpenAI
    _model: str = getenv("UNC_OPENAI_MODEL", default="gpt-4o-mini")

    def __init__(self, client: Annotated[AzureOpenAI, Depends(openai_client)]):
        """Initialize the OpenAI service with configuration from environment variables.

        Reads API key, version, and endpoint from environment variables and
        configures the Azure OpenAI client.
        """
        self._client = client

    def prompt(
        self, system_prompt: str, user_prompt: str, response_model: Type[T]
    ) -> T:
        """Send a prompt to the AI and parse the response into the specified model.

        Args:
            system_prompt (str): Instructions for the AI's behavior.
            user_prompt (str): The user's query or input to the AI.
            response_model (Type[T]): A Pydantic model class that defines the
                expected structure of the response.

        Returns:
            T: An instance of the response_model populated with the AI's response.

        Raises:
            ValueError: If the API response doesn't contain valid content.
        """
        completion = self._client.beta.chat.completions.parse(
            model=self._model,
            response_format=response_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        if (
            not completion.choices
            or not completion.choices[0].message
            or not completion.choices[0].message.content
        ):
            raise ValueError("Invalid response from the OpenAI API")
        else:
            return response_model.model_validate_json(
                completion.choices[0].message.content
            )
