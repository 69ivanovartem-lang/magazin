from dataclasses import dataclass
from typing import Optional

@dataclass
class products:
    id: Optional[int] = None
    price: float = 0.0
    name: str = ""
    count: int = 0
    quality: str = 0