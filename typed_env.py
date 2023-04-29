import datetime
from enum import Enum
from json import loads
from typing import Any, Callable, Optional

from dotenv import dotenv_values


def int_validator(value: Optional[str]) -> int:
    if value is None:
        raise ValueError("Value is None")
    return int(value)


def optional_int_validator(value: Optional[str]) -> Optional[int]:
    return None if value is None else int(value)


def str_validator(value: Optional[str]) -> str:
    if value is None:
        raise ValueError("Value is None")
    return value


def optional_str_validator(value: Optional[str]) -> Optional[str]:
    return None if value is None else value


def datetime_validator(value: Optional[str]) -> datetime.datetime:
    if value is None:
        raise ValueError("Value is None")
    try:
        # iso format
        return datetime.datetime.fromisoformat(value)
    except ValueError as e:
        try:
            return datetime.datetime.fromtimestamp(int(value))
        except ValueError as f:
            raise f from e


def optional_datetime_validator(value: Optional[str]) -> Optional[datetime.datetime]:
    try:
        return datetime_validator(value)
    except ValueError:
        return None


def dict_validator(value: Optional[str]) -> dict:
    if value is None:
        raise ValueError("Value is None")
    return loads(value)


def optional_dict_validator(value: Optional[str]) -> Optional[dict]:
    return None if value is None else loads(value)


def timedelta_validator(value: Optional[str]) -> datetime.timedelta:
    if value is None:
        raise ValueError("Value is None")
    return datetime.timedelta(seconds=int(value))


def optional_timedelta_validator(value: Optional[str]) -> Optional[datetime.timedelta]:
    return datetime.timedelta(seconds=int(value)) if value is not None else None


def bool_validator(value: Optional[str]) -> bool:
    if value is None:
        raise ValueError("Value is None")
    try:
        return bool(int(value))
    except ValueError as e:
        try:
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            else:
                raise ValueError("Value is not a boolean")
        except ValueError as f:
            raise f from e


def optional_bool_validator(value: Optional[str]) -> Optional[bool]:
    return None if value is None else bool_validator(value)


default_validators: dict[object, Callable[[Optional[str]], Any]] = {
    int: int_validator,
    Optional[int]: optional_int_validator,
    str: str_validator,
    Optional[str]: optional_str_validator,
    datetime.datetime: datetime_validator,
    Optional[datetime.datetime]: optional_datetime_validator,
    datetime.date: datetime_validator,
    Optional[datetime.date]: optional_datetime_validator,
    datetime.timedelta: timedelta_validator,
    Optional[datetime.timedelta]: optional_timedelta_validator,
    dict: dict_validator,
    Optional[dict]: optional_dict_validator,
    bool: bool_validator,
    Optional[bool]: optional_bool_validator,
}


class TypedEnv:
    """
    This class consists of methods to load environment variables from .env file.
    You should subclass this class then add your own types and default values.
    Only supported types are\n
    int\n
    str\n
    datetime.datetime \n
    dict (JSON)\n
    bool\n
    But you can extend it with your own type converters by using add_validator method with a type and a function that takes string (optionally).
    Or you can overwrite the validators dict to your own!
    """

    types: dict[str, object] = {}
    validators: dict[object, Callable[[Optional[str]], object]] = {}

    def __init_subclass__(cls) -> None:
        cls.types = {}

        for key, value in cls.__annotations__.items():
            cls.types[key] = value
        cls.validators.update(default_validators)

    def load(self, dotenv: Optional[str] = None, **kwargs) -> None:
        envs = dotenv_values(dotenv_path=dotenv, **kwargs)
        successful = {}
        for key, value in envs.items():
            if key in self.types:
                print("it's in the type!")
                try:
                    value = self.validators[self.types[key]](value)
                    print(f"got the type validated! {value}")
                except ValueError as e:
                    raise ValueError(f"Error while parsing {key}.") from e
                except KeyError as e:
                    raise ValueError(f"Unknown type {self.types[key]}") from e
                if value is not None:
                    print("value is not none")
                    setattr(self, key, value)
                    successful[key] = value
                else:
                    if not hasattr(self, key) and self.types[key] is not Optional:
                        raise ValueError(f"Variable {key} was not set!")
                    elif not hasattr(self, key) and self.types[key] is Optional:
                        setattr(self, key, None)
                print("continue!")
                continue
            raise ValueError(f"Unknown type {self.types[key]}")
        # now we check if any enviroment variable were not used and any variable that we didn't set
        for key, value in self.types.items():
            if key not in successful:
                if value is not Optional:
                    raise ValueError(f"Variable {key} was not set!")
                else:
                    if hasattr(self, key):
                        continue
                    else:
                        setattr(self, key, None)

    def add_validator(
        self, type_: object, validator: Callable[[Optional[str]], object]
    ) -> None:
        self.validators[type_] = validator
