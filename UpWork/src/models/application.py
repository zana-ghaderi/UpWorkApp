from pydantic import BaseModel
class Application(BaseModel):
    id: int
    job_id: int
    user_id: int
    proposal: str