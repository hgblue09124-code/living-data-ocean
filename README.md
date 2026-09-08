# Underworld v0 — Python Simulation Skeleton

**Underworld v0** là một thế giới tính toán (computational world) tối giản, thuần Python, nhẹ nhàng, tự vận hành và hỗ trợ quyền quản trị ở từng bước thời gian.

---

## 1. Underworld là gì?

Underworld là thế giới mô phỏng bên trong (internal world). Nó đại diện cho môi trường chứa trạng thái thế giới (`WorldState`), các thực thể (`Human`), và quy luật chuyển đổi trạng thái theo thời gian thông qua các sự kiện (`Events`).

Underworld được thiết kế cực kỳ nhẹ, không phụ thuộc vào bất kỳ thư viện hay framework nặng nề nào (không PyTorch, không TensorFlow, không LLM, không Mesa, không SimPy, không GPU, không server, không Docker). Bạn có thể dễ dàng tải repository về thiết bị cá nhân (kể cả di động như iPhone 12 Pro Max chạy ứng dụng Python) và khởi chạy ngay lập tức.

---

## 2. Ba Khái niệm Phân biệt: Con người, Agent bên ngoài và Quản trị viên

Trong Underworld v0 (PR #3), 3 vị trí được thiết kế tách biệt và có vai trò rõ ràng:

1. **Con người (Human):**
   - Là thực thể sinh học/nhân vật được mô phỏng bên trong thế giới.
   - Nằm trong danh sách quản lý của World (`world.humans`).
   - Tự động ra quyết định hành động dựa trên nhu cầu nội tại (`năng_lượng`, `đói`, `xã_hội`).

2. **Agent bên ngoài (External Agent):**
   - Là tác nhân bên ngoài tương tác với thế giới qua ranh giới nghiêm ngặt: nhận **`Observation`** và trả về **`Action`**.
   - Không được phép can thiệp trực tiếp vào biến nội tại của thế giới.

3. **Quản trị viên (QuanTriVien / Administrator):**
   - Là quyền điều khiển thế giới từ bên ngoài.
   - **KHÔNG phải là Con người** và không nằm trong danh sách thực thể mô phỏng.
   - Được gọi ở **MỖI bước thời gian** (`tai_moi_buoc`) để quan sát và có cơ hội can thiệp:
     - Thay đổi trạng thái môi trường.
     - Tạo sự kiện quản trị.
     - Tác động trực tiếp đến thực thể Con người.
     - Yêu cầu tạm dừng hoặc dừng mô phỏng (`yeu_cau_dung`).

---

## 3. Kiến trúc Ranh giới Giao tiếp

```
                  QUẢN TRỊ VIÊN (QuanTriVien)
                        │
                  tại_mỗi_bước()
                        ▼
              ┌─────────────────┐
              │     THẾ GIỚI    │
              │   (Underworld)  │
              │                 │
              │  WorldState     │
              │  Con người      │
              │  Môi trường     │
              │  Sự kiện        │
              └────────┬────────┘
                       │
                  Observation
                       │
                       ▼
                 EXTERNAL AGENT
                       │
                     Action
                       │
                       └──────► Thế giới
```

---

## 4. Chế độ Chạy Mô phỏng: Liên tục & Giới hạn

`EventLoop` hỗ trợ hai chế độ chạy linh hoạt:

1. **Chạy liên tục vô hạn (`chay()` / `chay(so_buoc=None)`):**
   - Thế giới tự động vận hành liên tục qua các bước $t_0 \rightarrow t_1 \rightarrow t_2 \dots$
   - Chỉ dừng lại khi Quản trị viên gửi lệnh `yeu_cau_dung()`.

2. **Chạy giới hạn số bước (`chay(so_buoc=N)`):**
   - Thế giới thực hiện đúng $N$ bước mô phỏng rồi kết thúc sạch sẽ.

---

## 5. Quy trình ở MỖI bước thời gian (Step Sequence)

Thứ tự thực thi ở từng bước thời gian được quy định xác định:

1. Xác định trạng thái hiện tại (`state_before`).
2. Quản trị viên quan sát qua `quan_tri_vien.tai_moi_buoc(state_before)`.
3. Áp dụng các tác động quản trị (nếu có).
4. Kiểm tra xem Quản trị viên có yêu cầu dừng không.
5. Thế giới thực hiện bước mô phỏng (`world.tick()`).
6. Tạo `Observation` cho External Agent và tiếp nhận `Action`.
7. Áp dụng `Action` từ External Agent.
8. Ghi nhận bước mô phỏng vào `Trajectory`.
9. Kiểm tra điều kiện kết thúc (Quản trị viên yêu cầu hoặc đạt `so_buoc`).

---

## 6. Hướng dẫn Khởi chạy Python

Dự án yêu cầu **Python 3.8+** tiêu chuẩn.

### Lệnh chạy mô phỏng Demo:

```bash
python main.py
```

### Lệnh chạy bộ kiểm thử tự động:

```bash
python -m unittest discover tests
```

hoặc bằng `pytest`:

```bash
PYTHONPATH=. pytest
```

---

## 7. Tệp dữ liệu đầu ra (Dataset)

Khi chạy demo `python main.py`, tập dữ liệu quỹ đạo mô phỏng được xuất tại:

```
data_output/dataset.jsonl
```

Tệp `dataset.jsonl` chứa các chuỗi `Trajectory` dạng JSON Lines, đảm bảo tính toàn vẹn ảnh chụp trạng thái (Snapshot Integrity) qua từng bước thời gian.
