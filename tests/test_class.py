import unittest

from timelessnesses.typed_env import TypedEnv


class MyDotEnv(TypedEnv):
    sex: bool = False


class TestClass(unittest.TestCase):
    def test_a(self):
        MyDotEnv().load("tests/valid.env")
        print(MyDotEnv.sex)
    
    def test_b(self):
        with self.assertRaises(ValueError):
            MyDotEnv().load("tests/invalid.env")
    
    def test_c(self):
        x = MyDotEnv()
        x.load("tests/valid.env")
        assert x.export_as_dict() == {"sex": True}


if __name__ == "__main__":
    unittest.main()
