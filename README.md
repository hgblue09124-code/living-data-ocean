# Underworld v0 — Python Simulation Skeleton

**Underworld v0** là một thế giới tính toán (computational world) tối giản, thuần Python, nhẹ nhàng và tự vận hành.

---

## 1. Underworld là gì?

Underworld là thế giới mô phỏng bên trong (internal world). Nó đại diện cho môi trường chứa trạng thái thế giới (`WorldState`), các thực thể (`Human`), và quy luật chuyển đổi trạng thái theo thời gian thông qua các sự kiện (`Events`).

Underworld được thiết kế cực kỳ nhẹ, không phụ thuộc vào bất kỳ thư viện hay framework nặng nề nào (không PyTorch, không TensorFlow, không LLM, không GPU, không server, không Docker). Bạn có thể dễ dàng tải repository về thiết bị cá nhân (kể cả di động như iPhone 12 Pro Max chạy ứng dụng Python) và khởi chạy ngay lập tức.

---

## 2. Tại sao thế giới có thể tự chạy?

Underworld sở hữu động cơ **Event Loop** nội tại.

Trong mỗi chu kỳ thời gian (tick):
1. Thế giới cập nhật các nhu cầu sinh học và trạng thái nội tại của mỗi `Human`.
2. Mỗi `Human` tự đưa ra quyết định hành động dựa trên quy luật và nhu cầu của riêng mình (như di chuyển, tìm thức ăn, nghỉ ngơi).
3. Thế giới xử lý các sự kiện tương tác giữa các `Human` (như gặp gỡ khi ở gần).
4. `WorldState(t)` chuyển đổi thành `WorldState(t+1)`.

Do đó, **ngay cả khi KHÔNG có Agent bên ngoài, Underworld vẫn tự vận hành liên tục**.

---

## 3. Human là gì?

Trong Underworld, **Human** ("Nhân") là một thực thể con người tồn tại bên trong thế giới mô phỏng (không phải mô-đun phần mềm nguyên tử `atomic software module`).

Mỗi Human sở hữu:
- `id`: Mã định danh duy nhất.
- `position`: Vị trí không gian $(x, y)$.
- `status`: Trạng thái hiện tại (ví dụ: `nghỉ_ngơi`, `di_chuyển`, `tìm_kiếm`, `gặp_gỡ`).
- `needs`: Các nhu cầu cơ bản (`năng_lượng`, `đói`, `xã_hội`).
- `goals`: Danh sách mục tiêu.
- `memory`: Ký ức ngắn hạn / lịch sử sự kiện.
- `action_history`: Lịch sử các hành động đã thực hiện.

---

## 4. Agent bên ngoài là gì?

**External Agent** (Agent bên ngoài) là một đối tượng nằm ngoài Underworld. Agent bên ngoài **KHÔNG phải là bộ não của thế giới**.

Ranh giới giao tiếp (boundary) được quy định nghiêm ngặt:
- Agent chỉ có thể **quan sát** thế giới thông qua **`Observation`**.
- Agent chỉ có thể **tác động** vào thế giới thông qua **`Action`**.
- Agent không được phép sửa đổi trực tiếp trạng thái nội tại của Underworld hay Human.

Sơ đồ kiến trúc ranh giới:

```
┌────────────────────────────────┐
│            UNDERWORLD          │
│                                │
│ World                          │
│   ↓                            │
│ WorldState                     │
│   ↓                            │
│ Humans                         │
│   ↓                            │
│ Events                         │
│   ↓                            │
│ State transitions              │
│   ↓                            │
│ New WorldState                 │
└────────────────────────────────┘
          │              ▲
     Observation       Action
          │              │
          ▼              │
┌────────────────────────────────┐
│         EXTERNAL AGENT         │
└────────────────────────────────┘
```

---

## 5. Pipeline hoạt động như thế nào?

Toàn bộ pipeline mô phỏng tuân theo luồng chuẩn:

$$\text{World} \rightarrow \text{WorldState} \rightarrow N \times \text{Human} \rightarrow \text{Event Loop} \rightarrow \text{Observation / Action} \rightarrow \text{Trajectory} \rightarrow \text{Dataset}$$

1. **World**: Khởi tạo không gian và danh sách $N$ Human.
2. **WorldState**: Lưu snapshot trạng thái tại thời điểm $t$.
3. **$N \times$ Human**: Thực hiện hành động tự chủ hoặc nhận lệnh ngoại cảnh.
4. **Event Loop**: Điều phối vòng lặp mô phỏng $t \rightarrow t+1$.
5. **Observation / Action**: Cung cấp góc nhìn cho Agent bên ngoài và nhận tác động ngoại cảnh.
6. **Trajectory**: Ghi lại chuỗi bước chuyển $(S_t, O_t, A_t, S_{t+1})$.
7. **Dataset**: Xuất tập dữ liệu ra tệp định dạng chuẩn JSONL.

---

## 6. Cách chạy bằng Python thuần

Dự án yêu cầu **Python 3.8+** tiêu chuẩn, không cần cài đặt thêm bất kỳ thư viện bên ngoài nào.

### Lệnh khởi chạy mô phỏng Demo:

```bash
python main.py
```

### Lệnh chạy bộ kiểm thử tự động:

```bash
python -m unittest discover tests
```

---

## 7. Dataset được sinh ra ở đâu?

Khi chạy lệnh `python main.py`, quá trình mô phỏng sẽ tự động ghi lại Trajectory và xuất Dataset ra tệp:

```
data_output/dataset.jsonl
```

Tệp `dataset.jsonl` chứa dữ liệu dạng văn bản JSON Lines, dễ đọc, dễ phân tích và có thể làm dữ liệu đầu vào cho các mô hình học máy sau này.

---

## Cấu trúc thư mục dự án

```
underworld/
├── world/
│   ├── __init__.py
│   ├── world.py
│   └── state.py
├── human/
│   ├── __init__.py
│   ├── human.py
│   └── state.py
├── engine/
│   ├── __init__.py
│   └── event_loop.py
├── interface/
│   ├── __init__.py
│   ├── observation.py
│   └── action.py
├── data/
│   ├── __init__.py
│   ├── trajectory.py
│   └── dataset.py
└── main.py
```
