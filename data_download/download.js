const axios = require('axios');
const fs = require('fs');

// --- CẤU HÌNH SCRIPT ---

// Cặp giao dịch bạn muốn tải
const SYMBOL = 'BTCUSDT'; 

// Các khung thời gian bạn muốn tải
const INTERVALS = ['1h', '4h', '12h', '1d'];

// Ngày bắt đầu tải dữ liệu (ĐỊNH DẠNG: YYYY-MM-DD)
// Script sẽ tải từ ngày này CHO ĐẾN HIỆN TẠI
const START_DATE_STRING = '2018-01-01'; 

// API endpoint (dùng Testnet hoặc Real đều được, dữ liệu lịch sử như nhau)
const API_URL = 'https://api.binance.com/api/v3/klines'; 

// Số mili giây trong một ngày (dùng để kiểm soát log)
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

// --- HẾT CẤU HÌNH ---


/**
 * Hàm sleep để tránh bị block API
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getTodayDateString() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Tháng bắt đầu từ 0
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
/**
 * Hàm gọi API Binance để lấy 1000 nến
 */
/**
 * Hàm gọi API Binance để lấy 1000 nến
 * SỬA ĐỔI: Dùng startTime thay vì endTime
 */
async function fetchKlines(symbol, interval, startTime, limit = 1000) {
  try {
    const params = {
      symbol: symbol,
      interval: interval,
      limit: limit,
      startTime: startTime // Luôn cung cấp thời gian bắt đầu
    };

    // Chỉ định endTime là thời gian hiện tại để tránh tải dữ liệu "tương lai" (nếu cần)
    // params.endTime = new Date().getTime(); 

    const response = await axios.get(API_URL, { params });
    return response.data; // response.data là một mảng các cây nến [cũ nhất ... mới nhất]
  } catch (error) {
    console.error(`Lỗi khi tải ${symbol}/${interval}:`, error.message);
    return []; // Trả về mảng rỗng nếu lỗi
  }
}

/**
 * Hàm chuyển đổi dữ liệu mảng của Binance sang định dạng CSV
 */
function formatDataForCsv(klines) {
  // Binance trả về: [Open time, Open, High, Low, Close, Volume, Close time, ...]
  // Chúng ta chỉ lấy các cột quan trọng
  return klines.map(kline => {
    const openTime = kline[0];
    const open = kline[1];
    const high = kline[2];
    const low = kline[3];
    const close = kline[4];
    const volume = kline[5];
    const closeTime = kline[6];
    
    // Trả về một chuỗi CSV
    return `${openTime},${open},${high},${low},${close},${volume},${closeTime}`;
  }).join('\n'); // Nối mỗi hàng bằng một dòng mới
}

/**
 * Hàm chính: Tải và lưu dữ liệu cho MỘT khung thời gian
 */
async function downloadAndSave(symbol, interval, overallStartTime) {
  const todayString = getTodayDateString(); 
  const fileName = `./${symbol}_${interval}_${START_DATE_STRING}_to_${todayString}.csv`;
  
  console.log(`\nBắt đầu tải: ${symbol} - ${interval}. Lưu vào ${fileName}`);
  
  // 1. Chuẩn bị file CSV và ghi tiêu đề (Headers)
  const headers = "open_time,open,high,low,close,volume,close_time\n";
  if (!fs.existsSync(fileName)) {
    fs.writeFileSync(fileName, headers);
  } else {
    console.log(`File ${fileName} đã tồn tại. Ghi đè...`);
    fs.writeFileSync(fileName, headers);
  }

  // 2. Logic vòng lặp (Pagination) MỚI
  // Bắt đầu từ `overallStartTime` và đi TIẾN VỀ HIỆN TẠI
  let currentStartTime = overallStartTime;
  const overallEndTime = new Date().getTime(); // Mốc thời gian hiện tại để dừng
  let totalCandlesDownloaded = 0;
  let lastLoggedTime = currentStartTime;

  // Lặp chừng nào thời gian bắt đầu của chúng ta còn cũ hơn thời gian hiện tại
  while (currentStartTime < overallEndTime) {
    
    // Gọi API để lấy 1000 nến *bắt đầu từ* `currentStartTime`
    const klines = await fetchKlines(symbol, interval, currentStartTime);

    if (klines.length === 0) {
      console.log(`[${interval}] Không còn dữ liệu (hoặc đã đến tương lai). Dừng lại.`);
      break; // Không còn dữ liệu, dừng lặp
    }
    
    // Dữ liệu trả về [oldest, ..., newest] đã được sắp xếp đúng
    const csvData = formatDataForCsv(klines);
    fs.appendFileSync(fileName, csvData + '\n'); // Ghi vào file

    totalCandlesDownloaded += klines.length;

    // Lấy thời gian đóng cửa của nến MỚI NHẤT (nến cuối cùng trong mảng)
    const lastCandleCloseTime = klines[klines.length - 1][6]; 
    
    // Cập nhật `currentStartTime` cho vòng lặp tiếp theo
    // Bắt đầu lần gọi tiếp theo ngay sau khi cây nến cuối cùng đóng cửa
    currentStartTime = lastCandleCloseTime + 1; // <-- Logic đi tới

    // In log tiến độ
    if (currentStartTime - lastLoggedTime > ONE_DAY_MS * 30) {
      lastLoggedTime = currentStartTime;
      const lastCandleDate = new Date(lastCandleCloseTime);
      console.log(`[${interval}] Đã tải về ${totalCandlesDownloaded} nến... (đến ngày ${lastCandleDate.toISOString()})`);
    }
    
    // QUAN TRỌNG: Chờ
    await sleep(500); 
  }

  console.log(`✅ [${interval}] Tải xong! Tổng cộng ${totalCandlesDownloaded} nến.`);
}

/**
 * Hàm chạy toàn bộ script
 */
async function runDownloader() {
  console.log("BẮT ĐẦU TẢI DỮ LIỆU LỊCH SỬ TỪ BINANCE");
  const overallStartTimeMs = new Date(START_DATE_STRING).getTime();

  // Lặp qua từng khung thời gian đã cấu hình
  for (const interval of INTERVALS) {
    // `await` đảm bảo chúng ta tải xong 1h mới đến 4h, ...
    // Điều này giúp giảm tải cho API và tránh bị block
    await downloadAndSave(SYMBOL, interval, overallStartTimeMs);
    await sleep(2000); // Chờ 2 giây trước khi sang khung thời gian mới
  }
  
  console.log("\nTẤT CẢ ĐÃ TẢI XONG");
}

// --- CHẠY KỊCH BẢN ---
runDownloader();