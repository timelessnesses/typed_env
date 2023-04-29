import unittest

from typed_env.typed_env import TypedEnv


class MyDotEnv(TypedEnv):
    sex: bool = False


class TestClass(unittest.TestCase):
    def test_a(self):
        MyDotEnv().load()


if __name__ == "__main__":
    unittest.main()
