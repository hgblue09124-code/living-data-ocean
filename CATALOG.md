# Living Data Ocean — Agent OS Module Seed Collection Catalog

## 📌 Tổng quan
Catalog này tổng hợp và chuẩn hóa các **Module Seeds** — tài nguyên ngữ nghĩa tái sử dụng dùng để làm nền tảng lắp ghép nên các năng lực của **Agent OS**.

Danh mục tuân thủ nghiêm ngặt nguyên tắc **Thu thập & Chuẩn hóa (Collection & Normalization Layer)**:
- ❌ Không chứa mã nguồn thực thi phần mềm (`index.py`, `test_module.py`).
- ❌ Không bắt buộc phải thu nhỏ khiên cưỡng "1 verb = 1 module".
- ✅ Chấp nhận các hạt hạt nhân ở đa dạng quy mô **Micro**, **Meso**, và **Macro**.
- ✅ Mỗi hạt seed mô tả đầy đủ 10 thuộc tính ngữ nghĩa: *name, purpose, semantic_boundary, scale, inputs, outputs, composition, source, evidence, assessment*.

---

## 📊 Thống kê Danh mục Seeds (Total: 27 Module Seeds)

### Phân loại theo Scale:
- 🟢 **Micro Seeds (24 hạt):** Các thao tác ngữ nghĩa nguyên tử đơn lẻ (ví dụ: `read`, `write`, `parse`, `check`, `store`).
- 🟡 **Meso Seeds (2 hạt):** Các cụm năng lực ngữ nghĩa cấp trung kết hợp nhiều micro seeds (ví dụ: `context-memory-session`, `tool-registry-lookup`).
- 🔴 **Macro Seeds (1 hạt):** Mô hình vòng lặp điều phối cấp cao kết nối các meso và micro seeds (`agent-execution-loop`).

---

## 🧩 Danh mục Chi tiết Module Seeds (`modules/`)

### 1. Nhóm Lưu trữ & Tệp tin (Storage & File Seeds)
| Name | Scale | Purpose | Primary Composition |
| :--- | :--- | :--- | :--- |
| `read-file-content` | Micro | Đọc nội dung tệp tin văn bản hoặc nhị phân từ đường dẫn tệp tin cục bộ. | Nối sang `parse-json-structured`, `extract-regex-pattern`, `diff-text-delta` |
| `write-file-content` | Micro | Ghi hoặc nối thêm dữ liệu văn bản/nhị phân vào đường dẫn tệp tin xác định. | Nối sau `transform-data-mapping` hoặc `agent-execution-loop` |
| `list-directory-entries` | Micro | Liệt kê các mục (tệp tin và thư mục con) trong một thư mục chỉ định. | Nối sang `find-file-path`, `read-file-content` |
| `find-file-path` | Micro | Tìm kiếm các đường dẫn tệp tin khớp với mẫu glob/fnmatch trong cây thư mục. | Nối sang `read-file-content`, `search-text-pattern` |
| `store-key-value` | Micro | Lưu trữ hoặc cập nhật một cặp khóa-giá trị vào đối tượng từ điển bộ nhớ trạng thái. | Kết hợp với `retrieve-key-value`, `state-transition-manager` |
| `retrieve-key-value` | Micro | Truy xuất giá trị từ một từ điển/map theo khóa một cách an toàn. | Nối sang `check-condition-predicate`, `route-conditional-target` |

### 2. Nhóm Xử lý Dữ liệu & Bóc tách (Data Processing & Extraction Seeds)
| Name | Scale | Purpose | Primary Composition |
| :--- | :--- | :--- | :--- |
| `parse-json-structured` | Micro | Parse chuỗi hoặc byte định dạng JSON thành cấu trúc dữ liệu Python. | Nối sau `read-file-content`, nối sang `query-json-path` |
| `extract-regex-pattern` | Micro | Bóc tách các chuỗi hoặc nhóm bắt tên khớp với biểu thức chính quy (regex) từ văn bản. | Nối sau `read-file-content`, nối sang `validate-schema-dict` |
| `query-json-path` | Micro | Truy vấn dữ liệu cấu trúc lồng nhau qua chuỗi đường dẫn phân cách bằng dấu chấm (dot-notation). | Nối sau `parse-json-structured`, nối sang `check-condition-predicate` |
| `transform-data-mapping` | Micro | Ánh xạ và chuyển đổi các trường dữ liệu giữa các dictionary dựa trên bản đồ cấu hình. | Chuyển đổi dữ liệu giữa các tool khác nhau |
| `inspect-object-schema` | Micro | Soi cấu trúc, kiểu dữ liệu và danh sách thuộc tính của một đối tượng dữ liệu trong bộ nhớ. | Nối sang `validate-schema-dict` |
| `detect-data-type` | Micro | Nhận diện định dạng ngữ nghĩa của chuỗi hoặc đối tượng (JSON, URL, Email, số, list). | Nối sang `route-conditional-target` |

### 3. Nhóm Kiểm tra & So sánh (Validation & Comparison Seeds)
| Name | Scale | Purpose | Primary Composition |
| :--- | :--- | :--- | :--- |
| `validate-schema-dict` | Micro | Xác minh dictionary có chứa đủ các trường bắt buộc và tuân thủ các ràng buộc kiểu dữ liệu. | Kiểm tra tham số trước khi gọi tool |
| `verify-data-hash` | Micro | Xác minh tính toàn vẹn của dữ liệu bằng cách tính toán và so sánh checksum hash. | Nối sau `read-file-content` để kiểm tra toàn vẹn file |
| `check-condition-predicate` | Micro | Đánh giá các mệnh đề so sánh logic trên dữ liệu (bằng, lớn hơn, chứa, khớp regex). | Nối sang `route-conditional-target`, `state-transition-manager` |
| `compare-object-equality` | Micro | So sánh hai đối tượng/cấu trúc dữ liệu để xác định sự bằng nhau tuyệt đối hoặc tương đương. | So sánh trạng thái Agent trước và sau hành động |
| `diff-text-delta` | Micro | Tính toán sự chênh lệch dòng văn bản (unified diff) giữa hai tài liệu hoặc chuỗi văn bản. | So sánh phiên bản code cũ và code mới |

### 4. Nhóm Điều khiển, Quan sát & Lập lịch (Control, Observation & Scheduling Seeds)
| Name | Scale | Purpose | Primary Composition |
| :--- | :--- | :--- | :--- |
| `route-conditional-target` | Micro | Điều hướng dữ liệu payload tới tập lệnh/đích xử lý tương ứng dựa trên bảng quy tắc điều kiện. | Nối sang `invoke-callable-handler` |
| `state-transition-manager` | Micro | Quản lý việc chuyển đổi trạng thái FSM (Finite State Machine) dựa trên hành động và bảng chuyển đổi. | Dùng trong `agent-execution-loop` quản lý vòng đời |
| `invoke-callable-handler` | Micro | Kích hoạt thực thi an toàn một hàm/callable với danh sách tham số truyền vào. | Nối sau `route-conditional-target` |
| `wait-time-interval` | Micro | Tạm dừng tiến trình thực thi trong một khoảng thời gian chỉ định. | Dùng chờ kết quả bất đồng bộ hoặc rate limiting |
| `select-candidate-option` | Micro | Lựa chọn phương án tốt nhất từ danh sách các ứng viên dựa trên tiêu chí cho trước. | Chọn tool tốt nhất hoặc chọn plan có điểm số cao nhất |
| `observe-system-state` | Micro | Quan sát thông tin môi trường và trạng thái hệ thống cục bộ (nền tảng, OS, PID, CWD). | Cung cấp ngữ cảnh môi trường cho Agent |
| `search-text-pattern` | Micro | Tìm kiếm vị trí và danh sách các dòng văn bản khớp với từ khóa hoặc mẫu regex. | Nối sau `read-file-content` |

### 5. Nhóm Quản lý Ngữ cảnh & Công cụ cấp Meso (Meso Seeds)
| Name | Scale | Purpose | Primary Composition |
| :--- | :--- | :--- | :--- |
| `context-memory-session` | Meso | Quản lý phiên ngữ cảnh bộ nhớ cho Agent, tích lũy lịch sử hội thoại và cắt tỉa theo window. | Kết hợp `store-key-value`, `retrieve-key-value`, cung cấp ngữ cảnh cho `agent-execution-loop` |
| `tool-registry-lookup` | Meso | Đăng ký, quản lý danh mục và tra cứu công cụ (tool/skill) khả dụng cho Agent. | Kết hợp `store-key-value`, `search-text-pattern`, cung cấp schema tool cho `agent-execution-loop` |

### 6. Nhóm Điều phối Vòng lặp Agent cấp Macro (Macro Seeds)
| Name | Scale | Purpose | Primary Composition |
| :--- | :--- | :--- | :--- |
| `agent-execution-loop` | Macro | Mô tả cơ chế vòng lặp suy luận và thực thi (ReAct) cốt lõi của Agent OS. | Điều phối `context-memory-session`, `tool-registry-lookup`, `invoke-callable-handler`, `route-conditional-target` |

---

## 🚫 Danh sách Bị Loại bỏ / Tiếng ồn (Removed Noise & Duplicates)
- **Mã thực thi phần mềm (`index.py`, `test_module.py`):** Đã loại bỏ hoàn toàn khỏi các thư mục hạt để đưa repository về đúng bản chất Collection Layer.
- **Workflow / Composite Skill đặc thù nghiệp vụ:** Đã loại bỏ các workflow tầng cao nghiệp vụ riêng lẻ không mang tính nền tảng tái sử dụng cho Agent OS.
