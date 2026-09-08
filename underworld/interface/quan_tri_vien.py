"""
Định nghĩa đối tượng QuanTriVien - Quyền điều khiển thế giới Underworld từ bên ngoài.
"""

from typing import Dict, List, Any, Optional
from underworld.world.state import WorldState
from underworld.interface.action import Action


class QuanTriVien:
    """
    Quản trị viên (Administrator) đại diện cho quyền điều khiển thế giới từ bên ngoài.

    Quản trị viên KHÔNG phải là một Con người (Human) trong thế giới.
    Quản trị viên được gọi ở MỖI bước thời gian thông qua phương thức `tai_moi_buoc(world_state)`.

    Quản trị viên có khả năng:
    - Thay đổi trạng thái môi trường
    - Tạo sự kiện
    - Tác động trực tiếp vào một Con người
    - Yêu cầu tạm dừng hoặc dừng hoàn toàn mô phỏng
    """

    def __init__(self, name: str = "QuanTriVien_HeThong"):
        """Khởi tạo Quản trị viên."""
        self.name = name
        self._yeu_cau_dung: bool = False
        self._lenh_cho_truoc: List[Dict[str, Any]] = []

    def yeu_cau_dung(self) -> None:
        """Gửi yêu cầu dừng mô phỏng thế giới."""
        self._yeu_cau_dung = True

    def dang_yeu_cau_dung(self) -> bool:
        """Kiểm tra xem Quản trị viên có đang yêu cầu dừng thế giới hay không."""
        return self._yeu_cau_dung

    def dat_lenh_tac_dong(self, lenh_list: List[Dict[str, Any]]) -> None:
        """Đặt danh sách các lệnh tác động sẽ thực thi ở lượt tiếp theo."""
        self._lenh_cho_truoc.extend(lenh_list)

    def tai_moi_buoc(self, trang_thai_the_gioi: WorldState) -> List[Dict[str, Any]]:
        """
        Điểm can thiệp chính thức của Quản trị viên ở MỖI bước thời gian.

        Phương thức này nhận vào trạng thái hiện tại của thế giới (trang_thai_the_gioi)
        và trả về danh sách các lệnh tác động quản trị (ví dụ: thay đổi môi trường,
        tạo sự kiện, tác động con người, hoặc dừng mô phỏng).
        """
        lenh_thuc_thi = list(self._lenh_cho_truoc)
        self._lenh_cho_truoc.clear()
        return lenh_thuc_thi

    def ap_dung_tac_dong_quan_tri(self, world: Any, lenh_list: List[Dict[str, Any]]) -> None:
        """
        Áp dụng trực tiếp danh sách lệnh của Quản trị viên lên đối tượng World.
        """
        for lenh in lenh_list:
            loai_lenh = lenh.get("loai_lenh")
            if loai_lenh == "THAY_DOI_MOI_TRUONG":
                key = lenh.get("key")
                val = lenh.get("val")
                if key:
                    world.environment[key] = val
            elif loai_lenh == "TAO_SU_KIEN":
                chi_tiet = lenh.get("chi_tiet", "Sự kiện từ Quản trị viên")
                world.tao_su_kien(chi_tiet, loai_su_kien="SU_KIEN_QUAN_TRI")
            elif loai_lenh == "TAC_DONG_CON_NGUOI":
                target_id = lenh.get("target_id")
                human = world.get_human(target_id)
                if human:
                    action_type = lenh.get("action_type", "REST")
                    payload = lenh.get("payload", {})
                    human.apply_external_action(action_type, payload)
            elif loai_lenh == "YEU_CAU_DUNG":
                self.yeu_cau_dung()
