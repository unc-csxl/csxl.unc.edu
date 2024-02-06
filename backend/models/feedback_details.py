from backend.models.feedback import Feedback

__authors__ = ["Matt Vu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class FeedbackDetails(Feedback):
    """
    Pydantic model to represent a `Feedback ticket`.

    This model is based on the `FeedbackEntity` model, which defines the shape
    of the `Feedback` database in the PostgreSQL database.
    """
