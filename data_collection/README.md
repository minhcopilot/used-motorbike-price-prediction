# Thu thập dữ liệu – Dự đoán giá xe máy cũ (Chợ Tốt Xe)

Người phụ trách: **Minh** · Người dùng dữ liệu: **Bảo**

## File giao cho Bảo
| File | Nội dung |
|---|---|
| `data/chotot_xemay_named.csv` | **File chính.** Dữ liệu thô toàn quốc, đã bỏ trùng `list_id`, có thêm cột tên hãng/dòng/loại/dung tích/xuất xứ. **Chưa làm sạch nhiễu** (để Bảo xử lý). |
| `data/chotot_xemay_raw.csv` | Giống trên nhưng chỉ có mã số, chưa có cột tên. |
| `data/mapping.csv` | Bảng ánh xạ mã → tên (`field`, `code`, `name`). |
| `data/regions.json` | Danh sách mã tỉnh/thành và số tin tại thời điểm crawl. |
| `data/raw/region_<mã>.csv` | Dữ liệu thô từng tỉnh. |
| `crawl.log` | Nhật ký chạy crawler. |

## Cách chạy lại
```
pip install requests pandas
python crawler.py
```
Crawler chạy tiếp được nếu bị ngắt (tỉnh nào đã có file trong `data/raw/` sẽ bỏ qua). Muốn crawl lại từ đầu thì xoá thư mục `data/`.

## Nguồn
- API danh sách: `https://gateway.chotot.com/v1/public/ad-listing?cg=2020&region_v2=<mã>&limit=50&o=<offset>`
- API chi tiết (lấy tên): `https://gateway.chotot.com/v1/public/ad-listing/<list_id>` → mảng `parameters`
- API trả tối đa 10.000 tin/truy vấn nên crawl theo từng tỉnh/thành.
- Nghỉ 1 giây giữa các request; robots.txt của xe.chotot.com cho phép crawler thông thường.
- **Không** thu thập tên, số điện thoại, ảnh, toạ độ của người bán.

## Từ điển dữ liệu (`chotot_xemay_named.csv`)
| Cột | Kiểu | Ý nghĩa | Ghi chú cho Bảo |
|---|---|---|---|
| `list_id` | int | Mã tin đăng | Khoá, đã bỏ trùng |
| `subject` | text | Tiêu đề tin | Có thể tách năm, tên dòng xe, từ khoá "chính chủ", "biển số đẹp", "zin" |
| `body` | text | Mô tả chi tiết | Nhiều teencode, emoji |
| `price` | int | **Giá (VNĐ) – biến mục tiêu** | Có giá ảo (rất nhỏ / rất lớn) |
| `price_string` | text | Giá dạng chữ | |
| `regdate` | int | Năm đăng ký | Tính tuổi xe; có thể có năm vô lý |
| `mileage_v2` | int | Số km đã đi | Có 0 km, số km vô lý |
| `motorbikebrand` / `brand_name` | mã / text | Hãng | |
| `motorbikemodel` / `model_name` | mã / text | Dòng xe | Có dòng "Khác"/"Dòng khác" |
| `motorbiketype` / `type_name` | mã / text | Loại xe (tay ga, xe số, côn tay...) | |
| `motorbikecapacity` / `capacity_name` | mã / text | Dung tích (nhóm) | |
| `motorbikeorigin` / `origin_name` | mã / text | Xuất xứ | Hay thiếu |
| `condition_ad`, `condition_ad_name` | mã / text | Mới / Đã sử dụng | Nên lọc chỉ giữ xe đã sử dụng |
| `region_v2`, `region_name` | mã / text | Tỉnh/thành | |
| `area_v2`, `area_name`, `ward_name` | mã / text | Quận/huyện, phường/xã | |
| `type` | text | `s` = bán, `k` = cần mua | Nên bỏ tin `k` nếu có |
| `is_price_not_valid` | bool | Chợ Tốt đánh dấu giá không hợp lệ | Dùng để lọc nhiễu |
| `number_of_images` | int | Số ảnh trong tin | Có thể dùng làm feature |
| `list_time`, `orig_list_time` | int (ms) | Thời điểm đăng / đăng gốc | Đổi bằng `pd.to_datetime(x, unit="ms")` |
| `crawl_date` | date | Ngày crawl | |

## Kết quả lần crawl 05/10/2026
- **30.563 tin** xe máy (sau khi bỏ 12 tin trùng `list_id`), **59 tỉnh/thành**, **30 cột**.
- Bảng ánh xạ: 602 mã → tên.
- TP.HCM có khoảng 15.000 tin, vượt trần 10.000/truy vấn, nên được chia theo 4 loại xe (tay ga, xe số, tay côn/moto, xe điện).

| Thống kê | Giá trị |
|---|---|
| Tỉnh nhiều tin nhất | TP.HCM 15.058 · Hà Nội 3.742 · Đà Nẵng 2.244 · Cần Thơ 1.795 · Đồng Nai 1.477 |
| Hãng | Honda 18.565 · Yamaha 5.326 · Piaggio 1.690 · Suzuki 882 · VinFast 764 · SYM 761 |
| Loại xe | Tay ga 16.664 · Xe số 7.050 · Tay côn/Moto 5.493 · Xe máy điện 1.356 |
| Dòng xe phổ biến | Air Blade 3.221 · SH 2.444 · Wave 2.098 · Vision 1.905 · Exciter 1.786 |
| Giá (VNĐ) | trung vị 19 triệu · Q1 10,5 triệu · Q3 34,5 triệu · max 13 tỷ (giá ảo) |

### Nhiễu đã phát hiện (để Bảo xử lý, chưa sửa trong file)
| Loại nhiễu | Số lượng |
|---|---|
| Giá < 2 triệu (có cả giá 0đ) | 115 |
| Giá > 500 triệu (đa số là giá ảo) | 44 |
| Xe **mới** lẫn trong dữ liệu | 462 |
| Số km = 0 | 780 |
| Số km > 500.000 | 333 |
| Thiếu số km | ~1,4% |
| Năm đăng ký = 0 hoặc < 1980 | 3 |
| Dòng xe "Dòng khác" (cần tách tên từ tiêu đề) | 1.835 |
| Thiếu xuất xứ / dung tích | 58% / 51% |
