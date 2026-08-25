from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    titre: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    priorite: int = Field(ge=1, le=3)


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    terminee: bool

    model_config = ConfigDict(from_attributes=True)