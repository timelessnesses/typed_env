import unittest
from enum import Enum
from typing import Optional

from timelessnesses.typed_env import Method, TypedEnv


class WeirdEnum(Enum):
    a = 0
    b = 1


class MyDotEnv(TypedEnv):
    sex: bool = False


class MyDotEnv2(TypedEnv):
    sex: bool = False
    weird: WeirdEnum


class TestClass(unittest.TestCase):
    def test_a(self):
        x = MyDotEnv()
        x.configure(Method.dotenv, dotenv="./tests/valid.env")
        x.load()
        assert x.sex

    def test_b(self):
        x = MyDotEnv()
        with self.assertRaises(ValueError):
            x.configure(Method.env, dotenv="./tests/invalid.env")
            x.load()

    def test_c(self):
        x = MyDotEnv()
        with self.assertRaises(ValueError):
            x.configure(Method.all)
            x.load()

    def test_d(self):
        x = MyDotEnv()
        with self.assertRaises(ValueError):
            x.configure(Method.dotenv, dotenv="./tests/invalid.env")
            x.load()

    def test_e(self):
        x = MyDotEnv()
        x.configure(Method.all, dotenv="./tests/valid.env")
        x.raise_error_on_unknown_env = False
        x.load()
        assert x.sex

    def test_f(self):
        x = MyDotEnv()
        x.configure(Method.dotenv, dotenv="./tests/valid.env")
        x.load()
        assert x.export_as_dict() == {"sex": True}

    def test_g(self):
        x = MyDotEnv2()
        x.configure(Method.dotenv, dotenv="./tests/valid2.env")
        x.add_validator(WeirdEnum, self.checker)
        x.load()
        assert x.weird == WeirdEnum.b

    def checker(self, value: Optional[str]) -> WeirdEnum:
        if value is None:
            raise ValueError("Value is None")

        return WeirdEnum(int(value))

    def test_h(self):
        x = MyDotEnv2()
        x.configure(Method.dotenv, dotenv="./tests/invalid2.env")
        x.add_validator(WeirdEnum, self.checker)
        with self.assertRaises(ValueError):
            x.load()


if __name__ == "__main__":
    unittest.main()
