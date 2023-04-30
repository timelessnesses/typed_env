import unittest

from timelessnesses.typed_env import TypedEnv, Method


class MyDotEnv(TypedEnv):
    sex: bool = False


class TestClass(unittest.TestCase):
    def test_a(self):
        x = MyDotEnv()
        x.get_env(Method.dotenv,dotenv="./tests/valid.env")
        x.load()
        assert x.sex
    
    def test_b(self):
        x = MyDotEnv()
        with self.assertRaises(ValueError):
            x.get_env(Method.env,dotenv="./tests/invalid.env")
            x.load()
            
    def test_c(self):
        x = MyDotEnv()
        with self.assertRaises(ValueError):
            x.get_env(Method.all)
            x.load()
            
    def test_d(self):
        x = MyDotEnv()
        with self.assertRaises(ValueError):
            x.get_env(Method.dotenv,dotenv="./tests/invalid.env")
            x.load()
    
    def test_e(self):
        x = MyDotEnv()
        x.get_env(Method.all, dotenv="./tests/valid.env")
        x.raise_error_on_unknown_env(False)
        x.load()
        assert x.sex
        
    def test_f(self):
        x = MyDotEnv()
        x.get_env(Method.dotenv, dotenv="./tests/valid.env")
        x.load()
        assert x.export_as_dict() == {"sex": True}


if __name__ == "__main__":
    unittest.main()
