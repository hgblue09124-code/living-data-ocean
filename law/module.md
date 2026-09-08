# Module Law — Quy luật & Triết lý Hạt Semantic Module

Tài liệu này đóng khung triết lý và cơ chế hoạt động của Module/Hạt đã được xác lập trong kho dữ liệu `living-data-ocean`. Đây là Module Law quy định cho cấp độ hạt semantic, không phải Global Law của toàn World.

---

## 1. Semantic Identity
* Hạt Module trước hết là một **semantic identity**.
* Tính chất Atomic không đồng nghĩa với một implementation nhỏ nhất hay một hàm code đơn lẻ.
* Tên của hạt là thành phần cốt lõi mang identity biểu diện bản chất của hạt đó.
* Không ép buộc semantic identity phải mang các nhãn dư thừa như `verb`, `noun`, `meaning`, `description` nếu chúng không thực sự cần thiết cho cấu trúc module.

---

## 2. Semantic Space
* Một Module sở hữu một không gian biểu hiện semantic **mở và đa chiều**.
* Một semantic identity có thể có nhiều biểu hiện, quan hệ và hướng kết hợp hợp lệ khác nhau.
* Không được đóng khung hay giới hạn identity vào một cặp input/output duy nhất.

---

## 3. Reference Projection
* Thuộc tính `reference_inputs` và `reference_outputs` chỉ đóng vai trò là **projection / tham chiếu**.
* Chúng không phải là semantic contract tuyệt đối hay ràng buộc bắt buộc.
* Không được sử dụng `reference_inputs` hay `reference_outputs` để phủ định các biểu hiện semantic hợp lệ khác của hạt.

---

## 4. Composition
* **Composition** là cơ chế cốt lõi để các semantic identity kết nối và hình thành nên các cấu trúc cao hơn.
* Composition phải bảo toàn tính chất quan hệ và **thứ tự**.
* Mối quan hệ có thứ tự `[A, B]` và `[B, A]` là hai quan hệ hoàn toàn khác nhau về mặt ngữ nghĩa.
* Meso là semantic composition đã kết tinh, không phải là một loại capability hoàn toàn khác biệt.

---

## 5. Atomic và Meso
* Atomic và Meso cùng thuộc về **một hệ thống Module đồng nhất**.
* Không tạo ra hai hệ thống schema hay định dạng riêng biệt giữa Atomic và Meso.
* Atomic là identity nền tảng; Meso là identity được hình thành từ composition của các identity khác.
* Composition của các Meso có thể tiếp tục tạo ra các cấu trúc ngữ nghĩa cao hơn.

---

## 6. Boundary
* Mỗi Module bắt buộc phải có **semantic boundary** (ranh giới ngữ nghĩa) rõ ràng.
* Không biến một Module thành nơi chứa tùy tiện nhiều capability không thuộc cùng một identity.
* Không tự ý mở rộng identity chỉ vì muốn giải quyết thêm một nhiệm vụ nghiệp vụ cụ thể.

---

## 7. Evolution
* Module có thể được dung nạp thêm các biểu hiện, mối quan hệ và kinh nghiệm tích lũy mới theo thời gian.
* Sự phát triển và mở rộng không được làm mất đi semantic identity ban đầu của hạt.
* Một implementation thực thi cụ thể không bao giờ được trở thành định nghĩa duy nhất của Module.

---

## 8. Admission
* Không phải mọi dữ liệu hay mã nguồn đều tự động trở thành Module trong Ocean.
* Vật liệu phải được tinh luyện, lọc bỏ nhiễu và đạt đầy đủ điều kiện semantic phù hợp trước khi trở thành hạt.
* Không tạo thêm Module chỉ để chạy theo số lượng hay quota.

---

## ⚠️ Các Sai Lệch Cần Tránh (Những lỗi không được tái phạm)

Để làm ghi nhớ bắt buộc cho các đợt thu gom và tinh luyện tiếp theo, tuyệt đối tránh các sai lệch sau:

1. **Không quay lại mô hình "Module = một capability hoàn chỉnh":** Không đồng nhất Atomic Module với một function implementation hay một chương trình chạy được.
2. **Không biến Module thành workflow/skill:** Không gom biến Module thành capability hay workflow nghiệp vụ hoàn chỉnh chỉ vì nó có thể thực hiện một nhiệm vụ.
3. **Không tạo mã thực thi:** Không tự tạo implementation Python, runtime, execution engine hay framework khi nhiệm vụ chỉ yêu cầu vật liệu semantic material.
4. **Không tạo Meso sai bản chất:** Không tạo Meso bằng cách ghép các capability cấp cao rồi gọi đó là cấu trúc atomic semantic.
5. **Không cứng nhắc Input/Output:** Không biến `reference_inputs`/`reference_outputs` thành contract bắt buộc hay khóa cứng kiểu dữ liệu.
6. **Không bỏ qua thứ tự Composition:** Không làm mất đi tính hướng và thứ tự trong mảng `compositions`.
7. **Không tạo Composition giả:** Không tạo composition chỉ để làm đẹp schema hoặc lấp chỗ trống khi không có quan hệ thực sự.
8. **Không tự thêm field/tag dư thừa:** Không thêm các thuộc tính, field hay nhãn (`verb`, `noun`, v.v.) chỉ vì cho rằng "đầy đủ hơn".
9. **Không chạy theo số lượng:** Không tự ý tạo module mới chỉ để tăng số lượng hoặc đạt chỉ tiêu hình thức.
10. **Không tự mở rộng phạm vi:** Tuyệt đối không tự ý thay đổi kiến trúc hoặc mở rộng nhiệm vụ khi chưa có chỉ thị trực tiếp từ cấp trên.
