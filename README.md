# typed-env

A python module that help you have a type safety on enviroment variable (on runtime)

## Documentation

```python
timelessnesses.TypedEnv
```

A parent class that will help you ensure type safetiness on your enviroment variable.  
Usage:

```python
from timelessnesses import typed_env
import datetime

class MyDotEnv(typed_env.TypedEnv):
    # define your enviroment variable name and it's type (default value is optional and typing.Optional is also supported)
    AMONG_US: bool = True
    DISCORD_TOKEN: str
    DATETIME: datetime.datetime = datetime.datetime.now()
    NICE_DICTIONARY: typing.Dict[str, int] = {"a": 1, "b": 2}
    DAMN_LIST: typing.List[int] = [1, 2, 3]
    BALLS_KIND: BallsEnum # oh no! TypedEnv doesn't support my custom class!
    # don't worry you can implement your own converter!

a = MyDotEnv()
a.add_validator(BallsEnum, lambda x: BallsEnum(int(x)))
a.get_env(typed_env.Method.dotenv, dotenv=".env") # you have options to either get only from dotenv or os.environ or both!
"""
a.get_env(typed_env.Method.all, dotenv="path_to_.env") # this fetch all the variable from both dotenv and os.environ
a.get_env(typed_env.Method.env) # this fetch all the variable from os.environ
a.get_env(typed_env.Method.dotenv, dotenv="path_to_.env") # this fetch all the variable from dotenv
NOTE: for dotenv/all method you have to supply dotenv argument
"""
a.raise_error_on_unknown_env(False) # if this set to true any excessive enviroment variable will raise an error (default is True)
a.load() # let it do the work!
```

`TypedEnv` supports normal types like `str` or `int` and also `typing.Dict` and `typing.List` etc. But it also supports custom type by adding a validator, you are also allowed to overwrite the default validator by using `TypedEnv.add_validator` method.  
Check out more examples at `tests` folder!
