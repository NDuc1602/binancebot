Mục tiêu của đề tài

Tìm hiểu công nghệ Blockchain và ứng dụng của nó trong giao dịch tiền điện tử.

Tìm hiểu và sử dụng Binance API (Testnet) để lấy dữ liệu thị trường và thực hiện lệnh giao dịch tự động.

Xây dựng ứng dụng Web gồm:

Front-end: giao diện điều khiển bot trading.

Back-end: kết nối với Binance Testnet, xử lý thuật toán trading và quản lý rủi ro.

Thiết kế thuật toán trading tự động đơn giản (ví dụ: SMA Crossover Strategy).

Triển khai và demo hệ thống thực tế, kiểm thử trên Binance Testnet.

🔗 Phạm vi và công nghệ sử dụng
Thành phần	Công nghệ	Mục đích
Blockchain	Binance Smart Chain (tham khảo)	Hiểu cơ chế lưu trữ & xác thực giao dịch
API Trading	Binance Spot Testnet API	Lấy dữ liệu & đặt lệnh mua/bán
Back-end	Node.js + Express + TypeScript	Giao tiếp với Binance API, xử lý logic
Front-end	React (Vite) / HTML / Chart.js	Hiển thị giá và điều khiển bot
Giao tiếp	REST API / WebSocket	Kết nối realtime giữa server và client
Quản lý code	GitHub Projects + Issues	Theo dõi tiến độ nhóm
Triển khai (tùy chọn)	Railway / Render / Docker	Deploy ứng dụng demo
⚙️ Kiến trúc hệ thống
┌────────────────────────────┐
│        Front-end (UI)      │
│  - Hiển thị giá & biểu đồ  │
│  - Nút Start/Stop Trading  │
│  - Lịch sử lệnh & PnL      │
└─────────────┬──────────────┘
              │ REST / WS
┌─────────────▼──────────────┐
│       Back-end Server      │
│  - Lấy dữ liệu từ Binance  │
│  - Tính toán tín hiệu SMA  │
│  - Gửi lệnh BUY/SELL       │
│  - Quản lý rủi ro          │
└─────────────┬──────────────┘
              │
┌─────────────▼──────────────┐
│     Binance Testnet API    │
│  - Cung cấp giá thị trường │
│  - Môi trường giả lập      │
└────────────────────────────┘


🤖 Thuật toán Trading (ví dụ: SMA Cross)

Ý tưởng:

Tính trung bình giá trong 2 khung thời gian:

SMA nhanh (fast) – ví dụ 7 nến gần nhất.

SMA chậm (slow) – ví dụ 25 nến gần nhất.

Khi đường SMA nhanh cắt lên đường chậm → mua (BUY).

Khi đường SMA nhanh cắt xuống đường chậm → bán (SELL).

Giới hạn rủi ro:

Không giao dịch khi lỗ quá MAX_DAILY_LOSS.

Giới hạn khối lượng tối đa MAX_OPEN_NOTIONAL.

📈 Kết quả mong đợi

✅ Ứng dụng web có thể lấy giá realtime từ Binance Testnet.

✅ Có thể thực hiện lệnh BUY/SELL tự động dựa trên tín hiệu SMA.

✅ Ghi log giao dịch, hiển thị biểu đồ và trạng thái bot.

✅ Có tài liệu hướng dẫn, báo cáo học thuật và video demo.
