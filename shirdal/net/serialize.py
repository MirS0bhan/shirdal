from abc import ABC, abstractmethod
from typing import Dict, Any, Type

from msgpack import packb, unpackb
from pydantic import BaseModel


class Serializer(ABC):
    @abstractmethod
    def serialize(self, item: Dict[Any, Any]):
        NotImplemented()

    @abstractmethod
    def deserialize(self, item: Dict[Any, Any] | bytes):
        NotImplemented()


class PydanticSerializer(Serializer):
    @classmethod
    def serialize(cls, item: BaseModel):
        return item.model_dump()

    @classmethod
    def deserialize(cls, item: Dict[Any, Any], model: Type[BaseModel]):
        return model(**item)


class MsgPackSerializer(Serializer):
    @classmethod
    def serialize(cls, item: Dict[Any, Any]) -> bytes:
        return packb(item)

    @classmethod
    def deserialize(cls, item: Dict[Any, Any]):
        return unpackb(item)

