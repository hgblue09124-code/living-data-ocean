# Underworld v0 — Pure Python Simulation Skeleton

**Underworld** là một thế giới mô phỏng tính toán (computational world) tối giản, thuần Python, tự vận hành hoàn toàn độc lập mà không phụ thuộc vào Agent bên ngoài, AI, LLM hay bất kỳ framework mô phỏng nặng nào.

Mục tiêu của dự án là tạo dựng một hạt nhân mô phỏng thế giới cực nhẹ, siêu sạch và linh hoạt để người dùng có thể tải về thiết bị cá nhân (như iPhone, iPad hay máy tính bàn), khởi chạy Python trực tiếp và quan sát thế giới mô phỏng qua giao diện Web UI di động.

---

## 1. Luồng Kiến trúc Cốt lõi (Architecture Pipeline)

Mô hình vận hành của Underworld v0 tuân thủ nghiêm ngặt chuỗi phân tầng một chiều:

```
                  Modules (Atomic & Meso)
                            ↓
                     World (Substrate)
                            ↓
                      World Program
                            ↓
                     World Graphics
                            ↓
                      UI Program
                            ↓
               Web UI (iPhone Safari / Browser)
```

1. **Modules (`underworld/modules/`):** Chứa các khả năng nguyên tử (Atomic Modules) và khả năng tầm trung (Meso Modules) như không gian, sinh học, môi trường, sự kiện và các UI Modules.
2. **World (`underworld/composition/world.py`):** Nền tảng thực thi (substrate) điều phối thế giới mô phỏng tự chủ.
3. **World Program (`underworld/composition/world_program.py`):** Lựa chọn, sắp xếp và tổng hợp các Modules thành một chương trình mô phỏng có thể thực thi (`Executable Program`).
4. **World Graphics (`underworld/graphics/world_graphics.py`):** Lọc các UI Modules, sắp xếp trật tự layout và tổng hợp thành `UIProgram`.
5. **UI Program (`underworld/graphics/ui_program.py`):** Xuất cấu trúc dữ liệu giao diện (Web presentation payload) không chứa logic mô phỏng.
6. **Web UI (`underworld/graphics/web_server.py`):** Web Server siêu nhẹ (dùng `http.server` chuẩn của Python) phục vụ giao diện Web responsive cho trình duyệt di động / desktop.

---

## 2. Hướng dẫn Khởi chạy Nhanh (Quick Start)

### Yêu cầu Môi trường
- Python 3.8+ (Không cần cài đặt thư viện ngoài ngoại trừ thư viện chuẩn Python).

### Khởi chạy Mặc định (Web UI Server)
Mở Terminal và gõ:

```bash
python3 main.py
```

hoặc khởi chạy qua package name:

```bash
python3 -m underworld
```

Terminal sẽ hiển thị thông báo:
```text
================================================================================
   UNDERWORLD v0 — WEB UI PROGRAM VIA WORLD GRAPHICS
================================================================================

[1] Hệ sinh thái Modules: Tổng số 18 Modules đã nạp.
[2] Đã tổng hợp World Program (Substrate: World | Runtime: EventLoop)
[3] World Graphics đã tổng hợp UI Program với 5 UI Modules.

------------------------------------------------------------
[4] BẮT ĐẦU WEB UI SERVER TẠI HOẠT ĐỘNG TẠI:
    👉 Máy tính nội bộ: http://localhost:8000
    📱 Trình duyệt iPhone / Mobile: http://192.168.x.x:8000
------------------------------------------------------------
```

---

## 3. Hướng dẫn Truy cập từ iPhone / Mobile (iPhone / Mobile Usage)

Bạn có thể dễ dàng khởi chạy và điều khiển mô phỏng Underworld trực tiếp từ điện thoại iPhone (hoặc bất kỳ thiết bị di động nào) theo các bước:

1. **Kết nối chung Mạng:** Đảm bảo điện thoại iPhone và máy tính chạy Underworld kết nối cùng một mạng Wi-Fi local.
2. **Khởi chạy Server:** Khởi chạy `python3 main.py` trên máy tính.
3. **Lấy địa chỉ IP LAN:** Nhìn vào dòng `📱 Trình duyệt iPhone / Mobile:` được in sẵn ở Terminal (ví dụ: `http://192.168.1.15:8000`).
4. **Mở Trình duyệt Safari:** Trên iPhone, mở Safari và truy cập địa chỉ IP trên.
5. **Quan sát & Tác động:**
   - Quan sát thời gian (Tick), thời tiết, chỉ số con người và dòng thời gian thực tế.
   - Bấm nút `⏭️ Bước Tiếp (1 Tick)`, `⏩ Chạy 10 Ticks`, hay gửi lệnh thời tiết `🌧️ Mưa lớn` từ Bảng điều khiển Quản trị viên.

---

## 4. Chế độ Console độc lập (Headless Mode)

Nếu muốn chạy mô phỏng hoàn toàn trong Terminal mà không cần bật Web UI Server (phù hợp cho các hệ thống kiểm thử CI/CD hay máy chủ không màn hình):

```bash
python3 main.py --headless --ticks 10
```

hoặc:

```bash
python3 -m underworld --headless --ticks 10
```

Chế độ Headless hoàn toàn độc lập, không khởi tạo Web Server và tiến hành tick mô phỏng trực tiếp trên console.

---

## 5. Cấu trúc Mô hình Module (Module System)

Toàn bộ các khả năng mô phỏng và thành phần giao diện đều tuân thủ quy tắc Module:

- **Atomic Modules (`underworld/modules/`):**
  - `SpatialSpace`: Vị trí không gian $x, y$.
  - `EntityNeeds`: Chỉ số sinh học (Năng lượng, Đói, Xã hội).
  - `EnvironmentState`: Môi trường và tài nguyên.
  - `EventLog`: Nhật ký sự kiện thế giới.
  - `CommandIntakeModule`, `ObservationBuilderModule`, `ActionResolverModule`, `StopPolicyModule`, `TrajectoryRecorderModule`.
- **Meso Module (`underworld/modules/meso/`):**
  - `SimulationEngineMeso`: Meso Module hợp thành từ 5 Atomic Modules đính kèm.
- **UI Modules (`underworld/modules/ui/`):**
  - `WorldStateViewModule`: Hiển thị chỉ số môi trường & thời gian.
  - `EntityViewModule`: Bảng thông tin thực thể con người.
  - `EventViewModule`: Danh sách sự kiện môi trường.
  - `TimelineViewModule`: Nhật ký diễn biến lịch sử.
  - `SimulationControlViewModule`: Bảng nút bấm điều khiển mô phỏng.

---

## 6. Xử lý Lỗi Thường gặp (Troubleshooting)

1. **iPhone Không Mở Được Trang Web:**
   - Kiểm tra xem iPhone và máy tính có đang bật chung Wi-Fi không.
   - Kiểm tra xem tường lửa (Firewall) trên máy tính có đang chặn cổng `8000` hay không.
2. **Muốn Đổi Cổng (Port) Khác:**
   - Bạn có thể đổi cổng chạy bằng cờ `--port`:
     ```bash
     python3 main.py --port 9000
     ```
3. **Lỗi `Address already in use`:**
   - Cổng 8000 đã bị chiếm bởi chương trình khác. Hãy đổi sang cổng khác bằng cờ `--port` hoặc giải phóng cổng 8000.

---

## 7. Chạy Bộ Kiểm thử Tự động (Testing)

Khởi chạy toàn bộ bộ kiểm thử tự động (Unit Tests & Integration Tests) của dự án bằng lệnh:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

Toàn bộ 33/33 bài kiểm thử sẽ vượt qua (OK) trong vòng chưa tới 10 giây.
