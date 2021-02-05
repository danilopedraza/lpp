from abc import (
    ABC,
    abstractmethod
)
from enum import (
    auto,
    Enum
)
from typing import Dict


class ObjectType(Enum):
    BOOLEAN = auto()
    ERROR = auto()
    INTEGER = auto()
    NULL = auto()
    RETURN = auto()


class Object(ABC):
    
    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass


class Integer(Object):
    
    def __init__(self, value: int) -> None:
        self.value = value
    
    def type(self) -> ObjectType:
        return ObjectType.INTEGER
    
    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):
    
    def __init__(self, value: bool) -> None:
        self.value = value
    
    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN
    
    def inspect(self) -> str:
        return 'verdadero' if self.value else 'falso'


class Null(Object):
    
    def type(self) -> ObjectType:
        return ObjectType.NULL
    
    def inspect(self) -> str:
        return 'nulo'


class Return(Object):

    def __init__(self, value: Object) -> None:
        self.value = value
    
    def type(self) -> ObjectType:
        return ObjectType.RETURN
    
    def inspect(self) -> str:
        return self.value.inspect()


class Error(Object):

    def __init__(self, message: str) -> None:
        self.message = message
    
    def type(self) -> ObjectType:
        return ObjectType.ERROR
    
    def inspect(self) -> str:
        return f'Error: {self.message}'


class Environment(Dict):
    
    def __init__(self):
        self._store = dict()
    
    def __getitem__(self, key):
        return self._store[key]
    
    def __setitem__(self, key, value):
        self._store[key] = value
    
    def __delitem__(self, key):
        del self._store[key]
