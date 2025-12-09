import os
from typing import Literal, overload


class GetEnvError(BaseException): ...


@overload
def get_env(name: str) -> str: ...
@overload
def get_env(name: str, *, strict: Literal[True]) -> str: ...
@overload
def get_env(name: str, *, strict: Literal[False]) -> str | None: ...
def get_env(name: str, *, strict: bool = True) -> str | None:
    value = os.getenv(name)

    if value is None and strict:
        msg = f"Env variable {name!r} does not exist"
        raise GetEnvError(msg)

    return value
