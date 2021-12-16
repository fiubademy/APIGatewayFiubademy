from pydantic.main import BaseModel
from typing import List, Optional


class OptionForQuestionReturn(BaseModel):
    number: int
    content: str
    #correct: str


class questionsContent(BaseModel):
    question_type: str
    question_content: str
    choice_responses: Optional[List[OptionForQuestionReturn]]