# Underworld v0 — Python Simulation Skeleton

**Underworld v0** là một thế giới tính toán (computational world) tối giản, thuần Python, nhẹ nhàng, tự vận hành độc lập và hỗ trợ giao diện điều khiển quản trị từ bên ngoài (External Human Control Interface).

---

## 1. Underworld là gì?

Underworld là thế giới mô phỏng bên trong (internal world). Nó đại diện cho môi trường chứa trạng thái thế giới (`WorldState`), các thực thể (`Human`), và quy luật chuyển đổi trạng thái theo thời gian thông qua các sự kiện (`Events`).

Underworld được thiết kế cực kỳ nhẹ, không phụ thuộc vào bất kỳ thư viện hay framework nặng nề nào (không PyTorch, không TensorFlow, không LLM, không Mesa, không SimPy, không GPU, không server, không Docker). Bạn có thể dễ dàng tải repository về thiết bị cá nhân (kể cả di động như iPhone 12 Pro Max chạy ứng dụng Python) và khởi chạy ngay lập tức.

---

## 2. Ba Khái niệm Phân biệt: Con người, Agent bên ngoài và Administrator

Trong Underworld v0, 3 vị trí được thiết kế tách biệt và có ranh giới kiến trúc rõ ràng:

1. **Con người (Human):**
   - Là thực thể sinh học/nhân vật được mô phỏng bên trong thế giới.
   - Nằm trong danh sách quản lý của World (`world.humans`).
   - Tự động ra quyết định hành động dựa trên nhu cầu nội tại (`năng_lượng`, `đói`, `xã_hội`).

2. **Agent bên ngoài (External Agent):**
   - Là tác nhân bên ngoài tương tác với thế giới qua ranh giới nghiêm ngặt: nhận **`Observation`** và trả về **`Action`**.
   - Không được phép can thiệp trực tiếp vào biến nội tại của thế giới.

3. **Giao diện Quản trị viên (Administrator):**
   - Là giao diện điều khiển của con người từ bên ngoài (External Human Control Interface).
   - **KHÔNG phải là Agent hay actor bên trong World**.
   - **World KHÔNG phụ thuộc vào Administrator để tự vận hành**.
   - Administrator tạo ra các **`AdministratorCommand`** trung gian gửi tới Runtime/World để thực hiện các tác động:
     - Thay đổi trạng thái môi trường (`CHANGE_ENVIRONMENT`).
     - Tạo sự kiện quản trị ngoài thế giới (`CREATE_EVENT`).
     - Tác động trực tiếp đến thực thể Con người (`AFFECT_HUMAN`).
     - Yêu cầu tạm dừng hoặc dừng mô phỏng (`REQUEST_STOP`).

---

## 3. Kiến trúc Ranh giới Giao tiếp (Boundary Architecture)

```
       ADMINISTRATOR (External Human Control Interface / UI)
                               │
                      AdministratorCommand
                               │
                               ▼
                            RUNTIME (EventLoop)
                               │
                               ▼
                     ┌──────────────────┐
                     │     THẾ GIỚI     │
                     │    (Underworld)  │
                     │                  │
                     │   WorldState     │
                     │   Con người      │
                     │   Môi trường     │
                     │   Sự kiện        │
                     └────────┬─────────┘
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

1. **Chạy liên tục vô hạn (`run()` / `run(steps=None)`):**
   - Thế giới tự động vận hành liên tục qua các bước $t_0 \rightarrow t_1 \rightarrow t_2 \dots$ mà không cần bất kỳ can thiệp nào.
   - Chỉ dừng lại khi nhận được lệnh `REQUEST_STOP` từ Administrator hoặc tín hiệu dừng từ hệ thống.

2. **Chạy giới hạn số bước (`run(steps=N)`):**
   - Thế giới thực hiện đúng $N$ bước mô phỏng rồi kết thúc sạch sẽ.

---

## 5. Hướng dẫn Khởi chạy Python

Dự án yêu cầu **Python 3.8+** tiêu chuẩn, không cần cài đặt thêm bất kỳ thư viện bên ngoài nào.

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

## 6. Tệp dữ liệu đầu ra (Dataset)

Khi chạy demo `python main.py`, tập dữ liệu quỹ đạo mô phỏng được xuất tại:

```
data_output/dataset.jsonl
```

Tệp `dataset.jsonl` chứa các chuỗi `Trajectory` dạng JSON Lines, đảm bảo tính toàn vẹn ảnh chụp trạng thái (Snapshot Integrity) qua từng bước thời gian.
