from pydantic import BaseModel, Field
from typing import Literal, Union

class GoToAction(BaseModel):
    action: Literal['goto']
    url: str

class ExtractAction(BaseModel):
    action: Literal['extract']
    selector: str

class SummarizeAction(BaseModel):
    action: Literal['summarize']
    text: str

Action = Union[GoToAction, ExtractAction, SummarizeAction]
