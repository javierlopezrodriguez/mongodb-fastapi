# Create models for API requests and responses
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from bson import ObjectId
from typing import Annotated, Any, Optional

# ObjectId Annotation to make it compatible with Pydantic
# https://stackoverflow.com/questions/76686267/what-is-the-new-way-to-declare-mongo-objectid-with-pydantic-v2-0
class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id, 
            core_schema.str_schema(), 
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

# Annotating ObjectId so that it behaves as a string for seralization purposes    
AnnotatedObjectId = Annotated[ObjectId, ObjectIdPydanticAnnotation]

# Model definition (Creation)
# To create an entry, every field (except id) is required
class Sepal(BaseModel):
    length: float = Field(..., description="Length of the sepal (required)")
    width: float = Field(..., description="Width of the sepal (required)")

class Petal(BaseModel):
    length: float = Field(..., description="Length of the petal (required)")
    width: float = Field(..., description="Width of the petal (required)")

class Flower(BaseModel):
    sepal: Sepal = Field(..., description="Sepal information (required)")
    petal: Petal = Field(..., description="Petal information (required)")
    species: str = Field(..., description="Species name (required)")
    id: AnnotatedObjectId = Field(alias="_id", description="Flower ID (generated)", default_factory=ObjectId)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "64c1d7c991e84e28c735a5c6",
                "sepal": {"length": 5.1, "width": 3.5},
                "petal": {"length": 1.4, "width": 0.2},
                "species": "Iris-setosa"
            }
        }

# Model definition (Update)
# To update an entry, every field is optional (and there is no id, that is not updatable)
class SepalUpdate(BaseModel):
    length: Optional[float] = Field(None, description="Length of the sepal")
    width: Optional[float] = Field(None, description="Width of the sepal")

class PetalUpdate(BaseModel):
    length: Optional[float] = Field(None, description="Length of the petal")
    width: Optional[float] = Field(None, description="Width of the petal")

class FlowerUpdate(BaseModel):
    sepal: Optional[SepalUpdate] = Field(None, description="Sepal information")
    petal: Optional[PetalUpdate] = Field(None, description="Petal information")
    species: Optional[str] = Field(None, description="Species name")

    class Config:
        json_schema_extra = {
            "example": {
                "sepal": {"length": 5.1, "width": 3.5},
                "petal": {"length": 1.4, "width": 0.2},
                "species": "Iris-setosa"
            }
        }
