from dataclasses import dataclass
from typing import Literal


@dataclass(kw_only=True, frozen=True, slots=True)
class Context:
    user_type: Literal["plus", "enterprise"] = "plus"
