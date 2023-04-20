from typing import Optional
import pydantic
from pydantic import BaseModel, Field, ValidationError
from bson import ObjectId


class Task(BaseModel):
    # id: ObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: str = Field(...)
    description: Optional[str] = Field(max_length=500)
    status: bool = Field(default=False, alias="completed")

    @pydantic.validator('status')
    @classmethod
    def valid_status(cls, value):
        allowed = ['0', 'off', 'f', 'false', 'n', 'no', '1', 'on', 't', 'true', 'y', 'yes', False, True]
        if value is not None and value not in allowed:
            raise ValueError("Invalid status value. Write 'yes' or 'no', please.")
        return value

    # @pydantic.root_validator(pre=True)
    # @classmethod
    # def check_the_task(cls, values):
    #     try:
    #         Task(title=values['title'], status=values['status'])
    #     except ValidationError as e:
    #         raise ValueError(str(e))
    #     return values

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[bool]

    @pydantic.validator('status')
    @classmethod
    def valid_status(cls, value):
        allowed = ['0', 'off', 'f', 'false', 'n', 'no', '1', 'on', 't', 'true', 'y', 'yes']
        if value is not None and value not in allowed:
            raise ValueError("Invalid status value. Write 'yes' or 'no', please.")
        return value

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True




