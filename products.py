from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    price: float = 0.0
    count: int = 0
    quality: str = ""