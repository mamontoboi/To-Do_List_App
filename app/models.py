from typing import Optional
import pydantic
from pydantic import BaseModel, Field
from bson import ObjectId


class BaseTask(BaseModel):
    title: None
    description: None
    status: None

    @pydantic.validator('status', pre=True)
    @classmethod
    def str_to_bool(cls, value):
        if value.lower() in ['0', 'off', 'f', 'false', 'n', 'no', 'False', 'not completed']:
            value = False
            return value
        elif value.lower() in ['1', 'on', 't', 'true', 'y', 'yes', 'True', 'completed']:
            value = True
            return value
        else:
            raise ValueError("Invalid status value. Write 'yes' or 'no', please.")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Task(BaseTask):
    title: str = Field(...)
    description: Optional[str] = Field(max_length=500)
    status: bool = Field(default=False)

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_the_task(cls, values):
        if not values["title"]:
            raise ValueError("The title is required")
        return values


class TaskUpdate(BaseTask):
    title: Optional[str]
    description: Optional[str]
    status: Optional[bool]


class TaskDetails(BaseModel):
    id: str
    title: str
    description: str
    status: str

    @pydantic.validator('status', pre=True)
    @classmethod
    def bool_to_str(cls, value):
        if isinstance(value, bool):
            return "completed" if value else "not completed"
        return value
