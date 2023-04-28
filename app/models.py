from typing import Optional, Union
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
        str_value = str(value).lower()
        false_values = ['0', 'off', 'f', 'false', 'n', 'no', 'False', 'not completed']
        true_values = ['1', 'on', 't', 'true', 'y', 'yes', 'True', 'completed']
        if str_value in false_values:
            value = False
            return value
        elif str_value in true_values:
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
        if not values.get("title"):
            raise ValueError("The title is required")
        return values


class TaskUpdate(BaseTask):
    title: Optional[str]
    description: Optional[str]
    status: Optional[Union[str, bool]]


class TaskDetails(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str

    @pydantic.validator('status', pre=True)
    @classmethod
    def bool_to_str(cls, value):
        # false_values = ['0', 'off', 'f', 'false', 'n', 'no', 'False', 'not completed']
        true_values = ['1', 'on', 't', 'true', 'y', 'yes', 'True', 'completed']
        if isinstance(value, bool):
            return "completed" if value else "not completed"
        if isinstance(value, str):
            return "completed" if value in true_values else "not completed"
        return value


