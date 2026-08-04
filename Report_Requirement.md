# Report Requirement: Traveloka Flight Booking System

Tài liệu này tổng hợp toàn bộ thông tin chi tiết về hệ thống **Traveloka Flight Booking & Management System**, bao gồm danh sách API, các tính năng nâng cao (Advanced Features), và các thư viện (Tech Stack) được sử dụng kèm theo lý do chọn lựa.

---

## 3. DANH SÁCH API (API ENDPOINTS)

Dưới đây là danh sách toàn bộ các API endpoint được triển khai trong hệ thống, chia theo nhóm chức năng:

### 🔑 Authentication (`/api/v1/auth`)

- **`POST /auth/signup`**: Đăng ký tài khoản người dùng mới. Đồng thời khởi tạo profile lưu trữ thông tin loyalty points (điểm tích lũy) và vai trò (role) của người dùng.
- **`POST /auth/signin`**: Đăng nhập hệ thống bằng email và mật khẩu qua Supabase Auth, trả về JWT token phục vụ xác thực.
- **`GET /auth/me`**: Lấy thông tin chi tiết của người dùng hiện tại (profile, loyalty points, avatar).
- **`PUT /auth/me`**: Cập nhật thông tin cá nhân của người dùng (tên hiển thị, avatar URL).
- **`PUT /auth/password`**: Thay đổi mật khẩu người dùng hiện tại.
- **`DELETE /auth/me`**: Xóa tài khoản người dùng hiện tại.
- **`GET /auth/admin-only`**: Endpoint kiểm tra quyền quản trị viên (Admin check).

### ✈️ Flights (`/api/v1/flights`)

- **`GET /flights`**: Lấy toàn bộ danh sách các chuyến bay.
- **`GET /flights/public`**: Lấy danh sách các chuyến bay sắp khởi hành công khai (lọc theo thời gian thực).
- **`GET /flights/{flight_id}`**: Lấy thông tin chi tiết của một chuyến bay cụ thể bằng ID.
- **`GET /flights/{flight_id}/occupied_seats`**: Lấy danh sách các ghế đã có người đặt trên chuyến bay để hiển thị sơ đồ ghế động.

### 📍 Airports (`/api/v1/airports`)

- **`GET /airports/all`**: Lấy danh sách tất cả các sân bay hỗ trợ trong hệ thống (SGN, HAN, DAD, CXR...).

### 🎫 Bookings (`/api/v1/bookings`)

- **`POST /bookings`**: Tạo yêu cầu đặt vé chuyến bay mới (trạng thái ban đầu là `pending`). Hỗ trợ tính toán tự động chiết khấu (discount) dựa trên cấp độ điểm tích lũy của khách hàng.
- **`PUT /bookings/{booking_id}/complete`**: Xác nhận hoàn tất thanh toán cho giao dịch đặt vé. Hệ thống tự động tính toán và cộng điểm tích lũy (Loyalty Points) vào profile của người dùng dựa trên loại ghế (Seat Class) và loại hành trình (One-way / Round-trip).
- **`GET /bookings/my_summary`**: Lấy danh sách tóm tắt toàn bộ vé đặt của người dùng hiện tại.
- **`GET /bookings/user_active`**: Lấy danh sách các giao dịch đặt vé đang hoạt động của người dùng hiện tại.
- **`GET /bookings/user/{user_id}`**: Lấy danh sách vé đặt cụ thể của một user.
- **`GET /bookings/admin_all`**: Lấy danh sách toàn bộ vé đặt hệ thống dành cho Admin quản trị.
- **`DELETE /bookings/{booking_id}`**: Hủy giao dịch đặt vé và giải phóng ghế tương ứng.
- **`POST /bookings/{booking_id}/like`**: Thích hoặc bỏ thích hãng hàng không liên quan đến chuyến bay đã đặt (chỉ dành cho các chuyến bay đã hoàn thành).
- **`POST /bookings/{booking_id}/comment`**: Thêm bình luận/phản hồi về trải nghiệm chuyến bay.
- **`GET /bookings/comments/list`**: Lấy danh sách các bình luận công khai.
- **`GET /bookings/airline_likes`**: Lấy thống kê số lượt thích cho từng hãng hàng không.

### 💵 Currency (`/api/v1/currency`)

- **`GET /currency/rates`**: Lấy tỷ giá quy đổi ngoại tệ hiện tại (tích hợp API tỷ giá thời gian thực).

### 👍 Likes (`/api/v1/likes`)

- **`GET /likes/status`**: Kiểm tra trạng thái thích của người dùng đối với một hãng hàng không hoặc chuyến bay cụ thể.
- **`GET /likes/summary`**: Tổng hợp số lượng lượt thích cho các hãng hàng không hàng đầu dựa trên các hành trình đã hoàn thành.

### 📝 Reviews (`/api/v1/reviews`)

- **`POST /reviews`**: Người dùng gửi đánh giá & điểm xếp hạng (ratings) cho chuyến bay.

### 📊 Analytics (`/api/v1/analytics`)

- **`GET /analytics/admin`**: Lấy các số liệu thống kê doanh thu, tỷ lệ đặt ghế, và các thông tin quản trị nâng cao.
- **`GET /analytics/dashboard-stats`**: Lấy dữ liệu tóm tắt nhanh cho dashboard admin (Doanh thu, Chuyến bay đang hoạt động, Tổng số vé đặt, Giá trị đơn hàng trung bình).
- **`GET /analytics/revenue-weekly`**: Lấy dữ liệu doanh thu theo tuần để vẽ biểu đồ tăng trưởng.

---

## 5. CÁC TÍNH NĂNG NÂNG CAO (ADVANCED FEATURES)

Dưới đây là danh sách đầy đủ các tính năng nâng cao được tìm thấy và hoạt động trong codebase:

1. **Real-time Seat Synchronization (Đồng bộ hóa ghế thời gian thực)**:
   - Sử dụng Supabase Realtime để đồng bộ hóa ngay lập tức các ghế đang được chọn hoặc thay đổi giữa các khách hàng khác nhau đang xem chung một chuyến bay, tránh việc chọn trùng ghế.
2. **User Presence Tracking (Theo dõi trạng thái hoạt động)**:
   - Hiển thị danh sách hoặc số lượng khách hàng hiện đang trực tuyến và cùng truy cập trong một "phòng đặt vé" (Flight booking room) bằng cơ chế Presence của Supabase.
3. **Real-time Broadcasting (Phát tin tức thời)**:
   - Tự động gửi thông báo hoặc tín hiệu cập nhật trạng thái (ví dụ: ghế vừa bị khóa hoặc vừa được giải phóng) tới tất cả các client đang kết nối mà không cần tải lại trang.
4. **Loyalty Points System (Hệ thống điểm thưởng & Chiết khấu)**:
   - _Quy tắc tích điểm_: Điểm thưởng được tính tự động dựa trên khoảng cách chuyến bay (Nội địa: 200 điểm, Quốc tế: 400 điểm) nhân với hệ số hạng ghế (First/Business: +50, Mid: +30, Economy: +20) và nhân đôi đối với vé khứ hồi.
   - _Ưu đãi thành viên_: Giảm giá vé dựa trên số điểm tích lũy hiện có của người dùng:
     - Tích lũy $\ge 5000$ điểm: Giảm 10%
     - Tích lũy $\ge 2000$ điểm: Giảm 5%
     - Tích lũy $\ge 1000$ điểm: Giảm 3%
5. **Dynamic Flight Crawling & Database Cleanup Daemon (Tiến trình cào & tự động dọn dẹp dữ liệu chuyến bay)**:
   - Sử dụng công cụ lập lịch (`schedule`) định kỳ tạo mới 1000 chuyến bay ngẫu nhiên và dọn dẹp các chuyến bay cũ hết hạn trong quá khứ (ngoại trừ những chuyến bay đã được đặt) để tối ưu dung lượng cơ sở dữ liệu.
6. **Dynamic Currency Exchange (Chuyển đổi ngoại tệ động)**:
   - Tích hợp API tỷ giá bên ngoài giúp người dùng dễ dàng chuyển đổi hiển thị giá vé máy bay giữa nhiều đơn vị tiền tệ phổ biến (USD, VND, EUR...) tức thời trên giao diện.
7. **Dynamic Geolocation (Tự động nhận diện vị trí người dùng)**:
   - Mock IP detection tự động xác định vị trí của người dùng để gợi ý sân bay gần nhất làm điểm khởi hành mặc định trong khung tìm kiếm.
8. **Interactive 2D Seating Chart (Sơ đồ ghế ngồi thông minh)**:
   - Sơ đồ máy bay 2D dạng 3-3 (gồm 120 ghế) với các trạng thái trực quan: Trống (Available - Xanh nhạt), Đang chọn (Selected - Cam neon nhấp nháy), Đã đặt (Occupied - Xám có dấu ✕). Hỗ trợ hiển thị buồng lái và lối thoát hiểm khẩn cấp.
9. **Airline Likes & Public Comments (Hệ thống thích & bình luận hãng bay)**:
   - Cho phép người dùng tương tác, bình luận, và thể hiện sự yêu thích đối với hãng bay sau khi hoàn tất chuyến bay, giúp tăng độ tin cậy của thông tin.
10. **Row-Level Security (RLS) & Multi-tenant Security Policies**:
    - Bảo vệ dữ liệu người dùng ở mức cơ sở dữ liệu (Supabase Postgres), đảm bảo khách hàng chỉ truy cập và chỉnh sửa được thông tin đặt vé hoặc profile cá nhân của chính họ, trong khi admin có quyền quản trị toàn cục.
11. **Comprehensive Admin Dashboard (Trang quản trị toàn diện)**:
    - Bảng điều khiển trực quan hiển thị biểu đồ doanh thu hàng tuần (sử dụng Chart.js), cùng danh sách CRUD chuyến bay và danh sách quản lý tất cả các đơn đặt vé.
12. **Custom SMTP Authentication Emailing**:
    - Cấu hình gửi email tự động (như xác nhận đăng ký tài khoản, gửi hóa đơn điện tử) thông qua máy chủ SMTP.
13. **Responsive UI & Page Transitions (Giao diện đáp ứng & chuyển trang mượt mà)**:
    - Layout chuẩn Traveloka tương thích tối đa từ thiết bị di động đến màn hình lớn, kết hợp hiệu ứng chuyển động tăng trải nghiệm người dùng (fade-in, hover lift effect, seating pulse).

---

## 6. THƯ VIỆN & CÔNG NGHỆ SỬ DỤNG (TECH STACK & LIBRARIES)

### 🎨 Frontend

- **Vue 3 (Composition API)**:
  - _Lý do chọn_: Framework xây dựng UI linh hoạt và tối ưu hiệu năng nhờ cơ chế Virtual DOM và reactivity system mạnh mẽ. Composition API giúp viết code gọn gàng, tái sử dụng các logic dưới dạng composables (ví dụ: `useNews`, `useWeather`).
- **Vite**:
  - _Lý do chọn_: Công cụ build frontend thế hệ mới với tốc độ Hot Module Replacement (HMR) cực nhanh, giúp nâng cao đáng kể trải nghiệm lập trình viên so với Webpack truyền thống.
- **Bootstrap 5 & SCSS**:
  - _Lý do chọn_: Cung cấp hệ thống Grid responsive mạnh mẽ và các components cơ bản nhanh chóng. Sử dụng SCSS cho phép định nghĩa các Design Tokens (màu sắc Traveloka, khoảng cách, font chữ) một cách nhất quán và dễ dàng bảo trì.
- **Axios**:
  - _Lý do chọn_: Thư viện HTTP client tin cậy, hỗ trợ interceptors để tự động đính kèm JWT token vào header, xử lý các lỗi xác thực tập trung (như lỗi 401/403) một cách đồng bộ.
- **Supabase JS SDK (`@supabase/supabase-js`)**:
  - _Lý do chọn_: Kết nối trực tiếp với backend Supabase từ client để lắng nghe các kênh Real-time (Seat Synchronization, Presence, Broadcast) mà không cần tự cấu hình WebSocket server phức tạp.
- **Pinia**:
  - _Lý do chọn_: Thư viện quản lý trạng thái (State Management) chính thức của Vue 3, nhẹ nhàng, hỗ trợ TypeScript tốt và dễ sử dụng hơn Vuex rất nhiều.
- **Chart.js & vue-chartjs**:
  - _Lý do chọn_: Thư viện vẽ biểu đồ nhẹ, đẹp mắt và dễ tùy biến, thích hợp để vẽ các biểu đồ phân tích doanh thu hàng tuần trên Admin Dashboard.

### ⚙️ Backend

- **FastAPI**:
  - _Lý do chọn_: Python Web Framework hiện đại, hiệu năng cực cao (nhờ ASGI và Uvicorn), tự động tạo tài liệu API tương tác (Swagger UI / ReDoc) giúp việc phát triển và tích hợp dễ dàng hơn bao giờ hết.
- **Pydantic & Pydantic Settings**:
  - _Lý do chọn_: Hỗ trợ kiểm tra kiểu dữ liệu (data validation) chặt chẽ và quản lý cấu hình dự án thông qua file `.env` một cách an toàn và nhất quán.
- **SQLAlchemy**:
  - _Lý do chọn_: Thư viện ORM (Object-Relational Mapping) mạnh mẽ nhất trong hệ sinh thái Python, giúp tương tác với cơ sở dữ liệu quan hệ một cách trừu tượng thông qua các class Python thay vì viết SQL thuần túy.
- **Uvicorn**:
  - _Lý do chọn_: Máy chủ chạy ứng dụng ASGI nhanh và nhẹ dành cho Python, tối ưu cho việc xử lý các kết nối bất đồng bộ (async/await) của FastAPI.
- **Supabase Python SDK (`supabase`)**:
  - _Lý do chọn_: Cho phép backend tương tác trực tiếp với cơ sở dữ liệu Postgres và dịch vụ Auth của Supabase một cách nhanh chóng và an toàn.
- **Schedule**:
  - _Lý do chọn_: Thư viện lập lịch tác vụ định kỳ đơn giản bằng Python để quản lý tiến trình chạy nền dọn dẹp database và đồng bộ chuyến bay tự động.
