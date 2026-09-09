# Underworld v0 — Python Simulation Skeleton

**Underworld v0** là một thế giới tính toán (computational world) tối giản, thuần Python, nhẹ nhàng, tự vận hành độc lập theo kiến trúc chuẩn **Atomic Semantic Modules → Composition → Meso Module → World Composition**.

---

## 1. Kiến trúc Mô phỏng Canonical (Canonical Architecture)

Thế giới được tổ chức theo các lớp mô-đun có ranh giới (boundary) và hướng phụ thuộc một chiều rõ ràng:

$$\text{Kernel} \longleftarrow \text{Modules} \longleftarrow \text{Composition} \longleftarrow \text{Runtime \& Interface} \longleftarrow \text{Data}$$

```
underworld/
├── kernel/                 # [Kernel] Các hạt nhân hạ tầng cốt lõi
│   ├── time.py             # SimulationTime: Quản lý thời gian t
│   ├── randomness.py       # Randomness: Quản lý RNG và hạt giống seed
│   └── identity.py         # EntityIdentity: Quản lý mã định danh
│
├── modules/                # [Modules] Các mô-đun chức năng độc lập (Atomic & Meso)
│   ├── spatial.py          # SpatialSpace: Tọa độ không gian (x, y) & khoảng cách
│   ├── environment.py      # EnvironmentState: Thuộc tính thời tiết & tài nguyên
│   ├── entity.py           # EntityNeeds: Chỉ số nhu cầu sinh học & ký ức
│   ├── event.py            # EventLog: Vòng đời sự kiện mô phỏng
│   ├── behavior.py         # EntityBehavior: Thuật toán ra quyết định tự chủ
│   ├── interaction.py      # InteractionRule: Quy tắc tương tác không gian
│   ├── command_dispatcher.py # CommandDispatcher: Tiếp nhận & phân phối lệnh quản trị
│   ├── command_intake.py   # CommandIntakeModule: Thu thập lệnh điều khiển
│   ├── observation_builder.py # ObservationBuilderModule: Dựng observation
│   ├── action_resolver.py  # ActionResolverModule: Xử lý agent actions
│   ├── stop_policy.py      # StopPolicyModule: Đánh giá dừng mô phỏng
│   ├── trajectory_recorder.py # TrajectoryRecorderModule: Ghi trajectory
│   └── meso/               # [Meso Modules ∈ Modules] Các Module tầm trung hợp thành từ Atomic Modules
│       └── simulation_engine.py # SimulationEngineMeso: Động cơ mô phỏng Meso
│
├── composition/            # [Composition] Tổng hợp cấu trúc mô phỏng
│   ├── state.py            # HumanState & WorldState
│   ├── human.py            # Human: Composition từ Identity, SpatialSpace, Needs, Behavior
│   ├── world.py            # World: Composition root điều phối các Atomic Modules qua delegation
│   └── simulation_loop.py  # SimulationLoopComposition: Composition hợp thành từ 5 Atomic Modules
│
├── runtime/                # [Runtime] Động cơ điều phối vòng lặp mô phỏng
│   └── event_loop.py       # EventLoop: Động cơ điều phối ủy quyền qua Meso Module
│
├── interface/              # [Interface] Ranh giới giao tiếp bên ngoài
│   ├── administrator.py    # Administrator: Giao diện điều khiển từ bên ngoài (External UI)
│   ├── command.py          # AdministratorCommand: Ranh giới lệnh quản trị
│   ├── observation.py      # Observation: Góc nhìn thế giới cho Agent
│   └── action.py           # Action: Tác động từ Agent vào thế giới
│
└── data/                   # [Data] Lưu trữ & Xuất tập dữ liệu mô phỏng
    ├── trajectory.py       # Trajectory & TrajectoryStep
    └── dataset.py          # Dataset (Xuất file JSONL)
```

---

## 2. Tiến hóa Kiến trúc: Atomic → Composition → Meso → World Composition

1. **Atomic Module:** Các khối khả năng nhỏ nhất có ranh giới rõ ràng (`CommandIntakeModule`, `ObservationBuilderModule`, `ActionResolverModule`, `StopPolicyModule`, `TrajectoryRecorderModule`).
2. **Composition:** Kết hợp các Atomic Modules để thử nghiệm tái lập hành vi điều phối vòng lặp mô phỏng (`SimulationLoopComposition`).
3. **Meso Module ($\text{Meso} \in \text{Modules}$):** Chuẩn hóa Composition ổn định thành Meso Module tầm trung (`SimulationEngineMeso` nằm trong `underworld/modules/meso/`).
4. **World Composition Root:** `World` và `EventLoop` sử dụng Meso Module `SimulationEngineMeso` để thực thi simulation lifecycle mà không biến World thành God Object.

---

## 3. Các Vai trò và Khái niệm trong Thế giới

1. **World (Thế giới):**
   - Là điểm gốc Composition của simulation.
   - Sở hữu trạng thái toàn cảnh (`WorldState`).
   - Tự vận hành độc lập qua cơ chế ủy quyền (delegation) đến các Atomic/Meso Modules mà không ôm toàn bộ logic.

2. **Agent (Tác nhân bên ngoài):**
   - Đại diện cho đối tượng tham gia tương tác bên trong thế giới (participant / decision-maker).
   - Nhận **`Observation`** và trả về **`Action`**.

3. **Administrator (Giao diện Quản trị viên):**
   - Đại diện cho giao diện điều khiển của con người từ bên ngoài (External Human Control Interface / UI).
   - **KHÔNG phải là Agent hay actor bên trong World**.
   - **World KHÔNG phụ thuộc vào Administrator để tự vận hành**.
   - Tạo ra các **`AdministratorCommand`** trung gian gửi tới Runtime/World:
     - `CHANGE_ENVIRONMENT`: Thay đổi thời tiết/tài nguyên.
     - `CREATE_EVENT`: Phát sinh sự kiện ngoài thế giới.
     - `AFFECT_HUMAN`: Can thiệp trực tiếp lên một Human.
     - `REQUEST_STOP`: Yêu cầu dừng mô phỏng.

---

## 4. Cách Chạy Mô phỏng: Bị chặn (Finite), Liên tục (Continuous) & Control Session

### A. Chạy bị chặn số bước (`run(steps=N)`):
```python
trajectory = event_loop.run(steps=10)
```

### B. Chạy liên tục (`run()` / `run(steps=None)`):
```python
trajectory = event_loop.run(steps=None, administrator=admin)
```

### C. Chạy phiên tương tác Control Session (`run_session()`):
```python
def session_controller(world_state):
    # Lựa chọn: CONTINUE, RUN_N_TICKS, COMMAND, OBSERVE, STOP
    return {"action": "RUN_N_TICKS", "ticks": 5}

trajectory = event_loop.run_session(session_controller=session_controller, administrator=admin)
```

---

## 5. Hướng dẫn Khởi chạy & Kiểm thử

Dự án yêu cầu **Python 3.8+** tiêu chuẩn.

### Lệnh chạy demo mô phỏng:

```bash
python main.py
```

### Lệnh chạy bộ kiểm thử tự động & benchmark:

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

Tệp `dataset.jsonl` được loại trừ trong `.gitignore`, đảm bảo tính toàn vẹn ảnh chụp trạng thái (Snapshot Integrity) qua từng bước thời gian.
