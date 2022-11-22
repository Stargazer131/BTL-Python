# Weather Forecast App

Một ứng dụng cơ bản để người dùng tìm thông tin về thời tiết của thành phố họ mong muốn tìm kiếm

### Phiên bản Desktop App

Các chức năng chính:

+ Hiển thị thời tiết tại thời điểm hiện tại
+ Hiển thị thời tiết tại vị trí hiện tại của người dùng
+ Hiển thị icon loại thời tiết
+ Hiển thị tên thành phố, quốc gia
+ Trạng thái thời tiết như độ ẩm, nhiệt độ, tốc độ gió
+ Tùy chỉnh độ C, độ F
+ Hình nền động thay đổi theo thời tiết
+ Dự báo thời tiết trong 7 ngày sắp tới

### Phiên bản Telegram Bot

Các chức năng chính:

+ Hiển thị thời tiết tại thời điểm hiện tại
+ Dự báo thời tiết trong 7 ngày sắp tới
+ Tự động cập nhật thông tin thời tiết ngày hôm nay vào 7 giờ sáng và ngày hôm sau vào 9 giờ tối
+ Tự động cảnh báo cho người dùng mỗi giờ một lần nếu như có hiện tượng thời tiết nguy hiểm hoặc bất tiện (chỉ từ 6 giờ sáng đến 9 giờ tối)
+ Dừng tự động cập nhật thông tin

## Buổi 1

### Tiến độ
+ Tổng hợp công việc 

| Mã SV - Họ tên   | Các nội dung thực hiện  | Thể hiện  | Ghi chú |
| :--------------- | :---------------------- |:----------|:---------|
| B20DCCN228 - Vũ Ngọc Hảo <br /> B20DCCN344 - Nguyễn Xuân Hưng | Từ ngày 09/09 đến ngày 30/09 | Main.py |         | 

+ Quá trình thực hiện

|STT |Phiên bản  | Vấn đề | Xử lý  | Tự đánh giá  |
|:---:|:----------|:-------|:-------|:-------------|
| 1 | 1.0 | Giao diện còn đơn giản chưa có nhiều chức năng | Phiên bản thử nghiệm hiển thị những chức năng cơ bản của một ứng dụng thời tiết. Toàn bộ chương trình chạy trong file Main.py | Ok |

### Yêu cầu

+ Tích hợp telegram hoặc một nền tảng nào đó cho phép giao tiếp 02 chiều với ứng dụng
+ Như vậy ứng dụng ngoài là một desktop app cần hoạt động như một service

## Buổi 2

### Tiến độ
+ Tổng hợp công việc 

| Mã SV - Họ tên   | Các nội dung thực hiện  | Thể hiện  |Ghi chú |
| :--------------- | :---------------------- |:----------|---------|
| B20DCCN228 - Vũ Ngọc Hảo | Từ ngày 12/10 đến ngày 06/11 | Main.py, Weather.py, Bot.py | |
| B20DCCN344 - Nguyễn Xuân Hưng | Từ ngày 12/10 đến ngày 06/11 | Main.py ||

+ Quá trình thực hiện

|STT |Phiên bản  | Vấn đề | Xử lý  |Thư viện/ Công cụ| Tự đánh giá  |
|:---:|:----------|:-------|:-------|:-------------|:-------------|
| 1 | 1.1 | + Ứng dụng mất nhiều thời gian để khởi động <br /> + Chưa linh hoạt trong việc tìm kiếm tên thành phố <br /> + Bị giới hạn bởi số lần gọi API (tối đa 1000/ngày) <br /> + Bot có thể gặp lỗi ngoài ý muốn nếu người dùng nhập sai cách | + Cài đặt lớp Weather lấy dữ liệu thời tiết, dữ liệu địa điểm thông qua lời gọi API <br /> + Cài đặt lớp Main là khung chương trình chính của desktop app <br /> + Cài đặt lớp Bot đóng vai trò là một Telegram Bot tương tác với người dùng| tkinter, python-telegram-bot, pytz, datetime, PIL, requests | Ok |

### Yêu cầu

+ Đóng gói thành window service và cảnh báo khi tới giờ được thiết lập hoặc khi có gì đấy cần thông báo

## Buổi 3

### Tiến độ
+ Tổng hợp công việc 

| Mã SV - Họ tên   | Các nội dung thực hiện  | Thể hiện  |Ghi chú |
| :--------------- | :---------------------- |:----------|---------|
| B20DCCN228 - Vũ Ngọc Hảo | Từ ngày 07/11 đến ngày 13/11 | Bot.py | |

+ Quá trình thực hiện

|STT |Phiên bản  | Vấn đề | Xử lý  |Thư viện/ Công cụ| Tự đánh giá  |
|:---:|:----------|:-------|:-------|:-------------|:-------------|
| 1 | 1.2 | + Có thể đóng gói thành window service nhưng không thể hiện thông báo | + Chuyển quá trình xử lý việc cảnh báo bằng window service sang bằng Telegram Bot <br /> + Cài đặt thêm một file exe để thuận tiện cho người dùng sử dụng <br /> + Đẩy bot lên sever để có thể chạy 24/7 | + nssm (Non sucking service manager) -> dùng để biến file exe thành window service <br /> + auto-py-to-exe -> dùng để biến project thành file exe <br /> + Website Python Anywhere (dùng để host Telegram Bot) | Chưa thực hiện theo đúng yêu cầu |
