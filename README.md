# Dự đoán giá xe máy cũ (Used Motorbike Price Prediction)

Đồ án môn **Khoa học dữ liệu**. Dự đoán giá bán xe máy cũ tại Việt Nam từ tin đăng trên Chợ Tốt Xe bằng các mô hình hồi quy.

## Thành viên
| Thành viên | Vai trò |
|---|---|
| Minh | Thu thập dữ liệu (crawler, từ điển dữ liệu, chương 2 báo cáo) |
| Bảo | Xây dựng model (EDA, xử lý nhiễu, feature, huấn luyện, đánh giá) |

Hạn nộp: **31/10/2026** – slide, báo cáo Word, kết quả.

## Cấu trúc
```
data_collection/   crawler.py + README (từ điển dữ liệu, thống kê nhiễu)   – Minh
data/raw/          dữ liệu thô: chotot_xemay_named.csv (file chính), mapping.csv
data/processed/    dữ liệu sau làm sạch                                     – Bảo
notebooks/         eda.ipynb, model.ipynb                                   – Bảo
models/            model đã train (.pkl)                                    – Bảo
app/               demo Streamlit (nếu có)
report/            báo cáo Word, slide
```

## Dữ liệu
- Nguồn: API công khai Chợ Tốt Xe, danh mục xe máy (`cg=2020`), crawl ngày 05/10/2026.
- **30.563 tin**, 59 tỉnh/thành, 30 cột. Biến mục tiêu: `price` (VNĐ).
- Dữ liệu **chưa làm sạch** – xem `data_collection/README.md` để biết các loại nhiễu.

```python
import pandas as pd
df = pd.read_csv("data/raw/chotot_xemay_named.csv")
```

## Chạy lại crawler
```
pip install requests pandas
cd data_collection
python crawler.py
```

## Quy ước làm việc
- Mỗi người làm trong thư mục của mình, `git pull` trước khi bắt đầu, commit nhỏ và ghi rõ nội dung.
- Không commit file tạm, file dữ liệu > 100 MB.
