from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    id: int
    title: str
    description: str
    budget: float
    currency: str
    user_id: int