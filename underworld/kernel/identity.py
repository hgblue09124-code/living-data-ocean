"""
Mô-đun Kernel quản lý định danh thực thể (EntityIdentity).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EntityIdentity:
    """
    Đại diện cho mã định danh duy nhất của thực thể.
    """
    id: str

    def __str__(self) -> str:
        return self.id
