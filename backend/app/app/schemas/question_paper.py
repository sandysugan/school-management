from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionPaperSchema(BaseModel):
    exam_id: int
    allocation_id: int
    subject_id: int
    uploaded_by: int
    file_path: str
    status: Optional[int] = 1

class BulkQuestionPaperSchema(BaseModel):
    question_papers: list[QuestionPaperSchema]
