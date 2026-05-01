from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress ="in_progress"
    done = "done"
    
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    status: TaskStatus = Field(TaskStatus.pending)
    
class TaskUpdate(BaseModel):
    title: str | None = Field(None,min_length=1,max_length=100)
    description: str | None = None
    status: TaskStatus | None
    
class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    completed_at: datetime | None
    
    model_config = {"from_attributes": True}