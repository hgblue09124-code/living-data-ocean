"""
Mô-đun Kernel quản lý tính ngẫu nhiên và hạt giống (Randomness).
"""

import random
from typing import Optional, List, Any


class Randomness:
    """
    Quản lý bộ sinh số ngẫu nhiên độc lập cho từng instance simulation.
    """

    def __init__(self, seed: Optional[int] = None):
        """Khởi tạo bộ sinh số ngẫu nhiên với seed tùy chọn."""
        self._seed = seed
        self._rng = random.Random(seed) if seed is not None else random.Random()

    def set_seed(self, seed: int) -> None:
        """Thiết lập seed ngẫu nhiên mới."""
        self._seed = seed
        self._rng = random.Random(seed)

    def choice(self, seq: List[Any]) -> Any:
        """Chọn ngẫu nhiên một phần tử trong danh sách."""
        return self._rng.choice(seq)

    def randint(self, a: int, b: int) -> int:
        """Sinh số nguyên ngẫu nhiên trong khoảng [a, b]."""
        return self._rng.randint(a, b)
