# Underworld v0 — Python Simulation Skeleton

**Underworld v0** là một thế giới tính toán (computational world) tối giản, thuần Python, nhẹ nhàng, tự vận hành độc lập và hỗ trợ giao diện điều khiển quản trị từ bên ngoài (External Human Control Interface).

---

## 1. World là gì?

**World (Thế giới)** đại diện cho môi trường mô phỏng bên trong (internal world).
World sở hữu:
- Trạng thái toàn cảnh của thế giới (`WorldState`).
- Danh sách các thực thể con người (`Human`).
- Biến môi trường (`environment`) và chuỗi sự kiện (`events`).
- Quy luật chuyển đổi trạng thái $t \rightarrow t+1$ thông qua phương thức `tick()`.

World được thiết kế cực kỳ nhẹ, không phụ thuộc vào bất kỳ thư viện hay framework nặng nề nào (không PyTorch, không TensorFlow, không LLM, không Mesa, không SimPy, không GPU, không server, không Docker).

---

## 2. Agent là gì?

**Agent (Tác nhân bên ngoài)** đại diện cho đối tượng tham gia tương tác bên trong thế giới.
- Agent quan sát thế giới qua ranh giới **`Observation`**.
- Agent tác động vào thế giới qua ranh giới **`Action`**.
- Agent quyết định hành động dựa trên góc nhìn quan sát được và tuân theo quy luật mô phỏng.

---

## 3. Administrator là gì & Tại sao Administrator KHÔNG phải Agent?

**Administrator (Giao diện Quản trị viên)** đại diện cho giao diện điều khiển của con người từ bên ngoài (External Human Control Interface).

### Tại sao Administrator KHÔNG phải là Agent?
1. **Khác biệt về vị trí:** Agent là một đối tượng tham gia mô phỏng (participant) bên trong thế giới. Administrator đứng hoàn toàn bên ngoài mô phỏng.
2. **Khác biệt về quyền hạn:** Agent chỉ được nhìn qua `Observation` và tác động qua `Action`. Administrator có quyền hạn tối cao từ bên ngoài (thay đổi thời tiết/môi trường, tạo sự kiện ngoài, can thiệp trạng thái, hoặc dừng mô phỏng).
3. **Khác biệt về sự phụ thuộc:** World tự vận hành liên tục mà **KHÔNG cần đến Administrator**.
4. **Không thuộc danh sách mô phỏng:** Administrator không nằm trong danh sách `world.humans` hay các actor của thế giới.

---

## 4. AdministratorCommand là gì?

**`AdministratorCommand`** là ranh giới lệnh trung gian (Command Boundary) chứa thông tin lệnh do Administrator tạo ra từ giao diện điều khiển / UI bên ngoài:

- `CHANGE_ENVIRONMENT`: Thay đổi thông số môi trường (thời tiết, tài nguyên...).
- `CREATE_EVENT`: Phát sinh một sự kiện ngoài thế giới.
- `AFFECT_HUMAN`: Can thiệp trực tiếp lên một Human cụ thể.
- `REQUEST_STOP`: Tín hiệu yêu cầu dừng vòng lặp mô phỏng.

Administrator **không sửa trực tiếp** bộ nhớ internal state của World, mà phát `AdministratorCommand` gửi tới Runtime/World để xử lý an toàn.

---

## 5. Kiến trúc Ranh giới Giao tiếp (Boundary Architecture)

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

## 6. Cách Chạy Mô phỏng: Bị chặn (Finite) & Liên tục (Continuous)

### A. Chạy bị chặn số bước (`run(steps=N)` / `chay(so_buoc=N)`):
Thế giới tiến hành đúng $N$ bước mô phỏng rồi kết thúc:
```python
trajectory = event_loop.run(steps=10)
```

### B. Chạy liên tục (`run()` / `run(steps=None)`):
Thế giới tự động vận hành liên tục qua các bước $t_0 \rightarrow t_1 \rightarrow t_2 \dots$ cho đến khi nhận được lệnh `REQUEST_STOP` từ Administrator:
```python
trajectory = event_loop.run(steps=None, administrator=admin)
```

### C. Cách gửi lệnh can thiệp (Intervention Command):
Từ giao diện Administrator bên ngoài:
```python
admin = Administrator()
admin.change_environment("weather", "bão_tuyết")
admin.create_event("Thiên thạch rơi")
admin.affect_human("Human_001", "REST")
admin.request_stop()
```

---

## 7. Hướng dẫn Khởi chạy & Kiểm thử

Dự án yêu cầu **Python 3.8+** tiêu chuẩn.

### Lệnh chạy demo mô phỏng:

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

## 8. Tệp dữ liệu đầu ra (Dataset)

Khi chạy demo `python main.py`, tập dữ liệu quỹ đạo mô phỏng được xuất tại:

```
data_output/dataset.jsonl
```

Tệp `dataset.jsonl` được bỏ qua trong theo dõi git (`.gitignore`), chứa các chuỗi `Trajectory` dạng JSON Lines, đảm bảo tính toàn vẹn ảnh chụp trạng thái (Snapshot Integrity) qua từng bước thời gian.
