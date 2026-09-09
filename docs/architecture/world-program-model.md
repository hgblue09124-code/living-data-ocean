# Mô hình Kiến trúc World, World Program & World Graphics

Tài liệu này ghi lại chính thức hợp đồng kiến trúc chuẩn (Architectural Contract) cho hệ thống **Underworld v0**, làm cơ sở định hướng cho các bước tiến hóa tiếp theo của mã nguồn.

---

## 1. Mục đích (Purpose)

Tài liệu này thiết lập mô hình khái niệm thống nhất giữa các thành phần: **Modules**, **World**, **World Program**, và **World Graphics**. Mục tiêu là giúp kho mã ghi nhớ rõ ràng vai trò của từng thành phần, đảm bảo World là một nền tảng thực thi (substrate) tự chủ, sạch sẽ và có thể mở rộng mà không bị biến thành một "God Object" hay một bộ mô phỏng đóng kín hard-code.

---

## 2. Sơ đồ Kiến trúc Tổng quan (Architecture Diagram)

```
                    Modules
                       │
             ┌─────────┴─────────┐
             │                   │
        Atomic Modules       Meso Modules
             │                   │
             └─────────┬─────────┘
                       ↓
                     World
                (load substrate)
                       │
              ┌────────┴────────┐
              ↓                 ↓
        World Program     World Graphics
              │                 │
              ↓                 ↓
       Executable Program     UI Program
                                  │
                                  ↓
                                User (Web UI / Mobile Browser)
```

---

## 3. Mô hình Module & Mối quan hệ Atomic vs Meso (Module Model)

### 3.1 Tất cả Khả năng là Modules
Toàn bộ các khả năng (capabilities) thực sự của mô phỏng phải được đại diện dưới dạng các Modules.

### 3.2 Đẳng cấp Module (First-Class Modules)
- $\text{Atomic Module} \in \text{Modules}$ (Module nguyên tử: khả năng sinh học, vị trí không gian, sự kiện, v.v.)
- $\text{Meso Module} \in \text{Modules}$ (Module tầm trung: được tổng hợp từ các Atomic Modules nhỏ hơn nhưng vẫn là một Module chính thức trong hệ sinh thái `underworld/modules/meso/`).

Meso Module **KHÔNG** phải là một tầng kiến trúc riêng biệt nằm ngoài hay nằm trên Modules, mà chỉ là một Module có quy mô tầm trung được tạo ra từ việc lắp ghép các Atomic Modules đã qua xác minh.

---

## 4. Mô hình World (World Substrate Model)

### 4.1 World là Nền tảng thực thi (Substrate)
**World** là một container ở cấp độ chương trình (program-level module / substrate). World cung cấp môi trường nền tảng để các Modules có sẵn tồn tại và cùng vận hành.

### 4.2 Không Hard-code Whitelist
World **KHÔNG** tự ý quyết định: *"chỉ những module này mới được phép hoạt động"*. World không sở hữu một danh sách whitelist đóng kín hard-code. Thay vào đó, World có khả năng khái niệm để tiêu hóa/nạp (digest/load) các Modules được cung cấp.

### 4.3 Trách nhiệm của World
World giữ vai trò điểm gốc Composition (Composition Root) cung cấp bề mặt thực thi ở cấp độ thế giới:
- Nạp và sở hữu trạng thái thế giới tổng hợp.
- Ủy quyền (delegation) các thao tác tính toán cho từng Module chức năng.
- Điều phối chu trình chuyển đổi trạng thái $t \rightarrow t+1$.

World **KHÔNG** trở thành:
- Bộ sinh hành vi ngẫu nhiên tự do.
- Động cơ phân tích dữ liệu.
- Bộ thực thi vòng lặp Runtime (`EventLoop`).
- Tập hợp chứa toàn bộ quy tắc nghiệp vụ mô phỏng.

---

## 5. Mô hình World Program (World Program Model)

Cần phân biệt rõ ràng giữa **World** (Substrate) và **World Program** (Chương trình thực thi cụ thể):

- **World:** Nền tảng mô phỏng chứa các thực thể và môi trường.
- **World Program:** Là kết quả của việc **lựa chọn + sắp xếp + tổng hợp** các Modules cụ thể thành một chương trình mô phỏng hoàn chỉnh có thể khởi chạy (`underworld/composition/world_program.py`).

Trách nhiệm lựa chọn và lắp ghép các Modules nằm ở bước dựng chương trình (Program-building responsibility), không được hard-code các quy tắc này thành một khối khổng lồ bên trong World.

---

## 6. Mô hình World Graphics (World Graphics Model)

### 6.1 Khái niệm World Graphics
**World Graphics** (`underworld/graphics/world_graphics.py`) chịu trách nhiệm xây dựng chương trình giao diện người dùng (UI Program) cho người vận hành từ các UI Modules có sẵn.

World Graphics **KHÔNG** chỉ đơn thuần là một bộ render hình ảnh (visual renderer).

### 6.2 Trách nhiệm khái niệm
$$\text{All Available Modules} \xrightarrow{\text{World Graphics: Filter + Order + Compose}} \text{UI Program} \xrightarrow{} \text{Web UI / Presentation}$$

World Graphics lọc, chọn lựa và sắp xếp các UI Modules để xây dựng một chương trình giao diện phù hợp nhất với góc nhìn và nhu cầu của từng đối tượng người dùng cụ thể. Giao diện người dùng do đó không phải là một cấu trúc màn hình cố định hard-code vĩnh viễn.

### 6.3 Một World — Nhiều UI Programs
Cùng một thế giới mô phỏng (World) và cùng một hệ sinh thái Modules có thể tạo ra các UI Programs hoàn toàn khác nhau cho các người dùng khác nhau:

- **Người dùng A (Operator Dashboard):**
  $$\text{Overview} \rightarrow \text{State} \rightarrow \text{Events} \rightarrow \text{Controls}$$

- **Người dùng B (Data Analyst Dashboard):**
  $$\text{Overview} \rightarrow \text{Analysis} \rightarrow \text{Timeline} \rightarrow \text{Controls}$$

Cả hai chương trình giao diện trên đều vận hành song song trên cùng một World bên dưới.

---

## 7. Đánh giá EventLoop & Ranh giới Runtime

### 7.1 Đánh giá EventLoop
`EventLoop` hiện tại (`underworld/runtime/event_loop.py`) đóng vai trò là động cơ điều phối Runtime. Trong kiến trúc mục tiêu:
- `EventLoop` có thể là một **Atomic Composition**, một **Meso Module** (`SimulationEngineMeso`), hoặc một **Composition linh hoạt** từ các Modules nhỏ hơn (`CommandIntakeModule`, `ObservationBuilderModule`, `ActionResolverModule`, `StopPolicyModule`, `TrajectoryRecorderModule`).
- `EventLoop` **KHÔNG** được coi mặc định là lõi kiến trúc bất biến vĩnh cửu, mà là một ứng viên thử nghiệm có thể tách và lắp ghép lại.

### 7.2 Ranh giới Runtime
Runtime chịu trách nhiệm điều phối vòng lặp (orchestration):
- Nhận lệnh (`Command Intake`).
- Dựng quan sát (`Observation Construction`).
- Xử lý tác động Agent (`Action Resolution`).
- Tiến hành bước (`Tick Execution`).
- Đánh giá dừng (`Stop Policy`).
- Ghi lịch sử (`Trajectory Recording`).

Runtime **KHÔNG** sở hữu trạng thái nghiệp vụ mô phỏng (Domain State) và không tự can thiệp trực tiếp làm biến đổi nhu cầu sinh học hay vị trí của con người.

---

## 8. Ranh giới Ảnh chụp Trạng thái (Snapshot Foundation)

Cơ chế `get_state()` hiện tại của World là hạ tầng chụp trạng thái (State-capture foundation), chưa phải là một hệ thống phân tích dữ liệu hoàn chỉnh.

Kiến trúc dành không gian cho ranh giới phân tích độc lập bên ngoài:
$$\text{World Snapshot}(t) \rightarrow \text{Comparison} \rightarrow \text{Transition} \rightarrow \text{Trajectory} \rightarrow \text{Analysis}$$

- Các snapshot lịch sử $S(t), S(t+1), S(t+N)$ hoàn toàn độc lập và không bị biến đổi khi thế giới chạy tiếp (`copy.deepcopy`).
- Logic phân tích quỹ đạo/sự kiện nằm hoàn toàn ở các mô-đun phân tích bên ngoài, không đưa logic phân tích vào bên trong World.

---

## 9. Định hướng Thế giới Định hình (Deterministic World Direction)

- **World** theo định hướng là một hệ thống định hình/xác định (structurally fixed & deterministic).
- Tính ngẫu nhiên/stochastic **KHÔNG** phải là thuộc tính tự nhiên mặc định gắn liền trong bản thân World, mà thuộc về các Modules hoặc dependencies rõ ràng (`Randomness`).
- Bảo tồn tính tái lập tuyệt đối:
  $$\text{Cùng cấu hình ban đầu} + \text{Cùng đầu vào} + \text{Cùng hạt giống seed} = \text{Cùng Trajectory 100\%}$$

---

## 10. Bảng Đối chiếu Thực tế Hiện tại vs Kiến trúc Mục tiêu

Bảng dưới đây đánh giá trung thực trạng thái hiện tại của mã nguồn Underworld v0 so với định hướng kiến trúc mục tiêu:

| Thành phần hiện tại (`Current Component`) | Vai trò hiện tại (`Current Role`) | Vai trò mục tiêu (`Target Role`) | Trạng thái đối chiếu (`Gap / Status`) |
| :--- | :--- | :--- | :--- |
| **`underworld/kernel/`** | Khả năng hạ tầng (Time, Randomness, Identity) | Primitives Infrastructure | **Đã tuân thủ** (`Implemented`) |
| **`underworld/modules/`** | Atomic Capabilities (Spatial, Needs, Event, Behavior, Interaction, CommandDispatcher...) | Atomic Semantic Modules | **Đã tuân thủ** (`Implemented`) |
| **`underworld/modules/meso/`** | `SimulationEngineMeso` tổng hợp từ 5 Atomic Modules | Meso Module ($\text{Meso} \in \text{Modules}$) | **Đã tuân thủ** (`Implemented`) |
| **`underworld/composition/world.py`** | Composition Root tạo World, ủy quyền cho Atomic/Meso Modules | Substrate / Program-level Container | **Thực nghiệm** (`Experimental` - Đã tách God Object, nhận nạp Modules) |
| **`underworld/runtime/event_loop.py`** | Điều phối vòng lặp mô phỏng & Control Loop Session | Runtime Orchestrator / Meso Candidate | **Đã tuân thủ** (`Implemented`) |
| **`underworld/interface/administrator.py`** | External Human Control Interface gửi `AdministratorCommand` | External Operator Interface | **Đã tuân thủ** (`Implemented`) |
| **`underworld/composition/world_program.py`** | Tổng hợp WorldProgram từ danh sách Modules | Program Assembly / Module Selector | **Đã tuân thủ** (`Implemented`) |
| **`underworld/graphics/world_graphics.py`** | Lọc, sắp xếp và tổng hợp UI Modules thành UIProgram | Module Selector + UI Program Composer | **Đã tuân thủ** (`Implemented`) |
| **`underworld/graphics/web_server.py`** | Server phục vụ giao diện Web responsive (Mobile Safari) | Web Presentation Server | **Đã tuân thủ** (`Implemented`) |
| **Snapshot Analytics Engine** | Đã có `get_state()` deep-copy snapshot bất biến | State-transition & Trajectory Analytics | **Đã lên kế hoạch** (`Planned` - Dành cho phiên bản sau) |

---

## 11. Cam kết Không Thực hiện (Explicit Non-Goals)

Trong nhiệm vụ lập tài liệu kiến trúc này, dự án **TUYỆT ĐỐI KHÔNG**:
1. Tự ý viết lại lớp `World` hoặc `EventLoop`.
2. Thêm các thư viện bên ngoài như Mesa, SimPy, PyTorch, LLM hay Database.
3. Xây dựng hệ thống Plugin Framework hay mã nạp động phức tạp quá mức.
4. Thay đổi bất kỳ hành vi mô phỏng hay bài kiểm thử nào đang hoạt động.
