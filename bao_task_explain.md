# Hướng dẫn chi tiết nhiệm vụ của Bảo

Tài liệu này giúp Bảo nắm bắt được các kiến thức cơ bản cần chuẩn bị và định nghĩa hoàn thành (Definition of Done) cho phần việc xây dựng mô hình dự đoán giá xe máy cũ.

## 1. Các kiến thức cốt lõi cần tìm hiểu (Base Concepts to Learn)

Trước khi bắt tay vào code, Bảo cần đảm bảo đã hiểu hoặc ôn tập lại các khái niệm sau:

### A. Phân tích dữ liệu khám phá (EDA - Exploratory Data Analysis)
- **Phân phối dữ liệu**: Hiểu về phân phối lệch phải (right-skewed) của giá xe và tại sao cần dùng biến đổi logarit (`log(price)`).
- **Trực quan hóa**: Biết cách dùng `matplotlib` và `seaborn` để vẽ biểu đồ phân phối (histogram), biểu đồ hộp (boxplot) để tìm outlier, và biểu đồ phân tán (scatterplot).
- **Ma trận tương quan**: Đánh giá sự tương quan giữa các biến số (ví dụ: tuổi xe, số km) với giá bán.

### B. Tiền xử lý dữ liệu (Data Preprocessing & Cleaning)
- **Xử lý Outliers (Nhiễu/Giá trị ngoại lai)**: Phương pháp IQR (Interquartile Range) để lọc giá ảo, hoặc dựa trên ngưỡng logic (ví dụ: giá < 2 triệu).
- **Xử lý Missing Data (Dữ liệu khuyết thiếu)**: Các kỹ thuật điền khuyết (Imputation) như điền bằng trung vị (median) theo nhóm tuổi, hoặc điền mode (giá trị xuất hiện nhiều nhất) theo dòng xe.
- **Biểu thức chính quy (Regex)**: Rất quan trọng để trích xuất thông tin từ đoạn text chứa tiêu đề (`subject`) như năm sản xuất thực tế, tên dòng xe bị ẩn trong "Dòng khác", hoặc các từ khóa "zin", "chính chủ".

### C. Kỹ thuật trích xuất đặc trưng (Feature Engineering)
- **Mã hóa biến phân loại (Categorical Encoding)**: Hiểu sự khác biệt và cách dùng One-hot Encoding (cho biến ít nhóm) và Target Encoding (cho biến nhiều nhóm như Tỉnh/Thành, Hãng xe).
- **Tạo biến mới**: Cách suy luận logic để tạo biến mới có ý nghĩa hơn (VD: `số km / tuổi xe` để biết mức độ sử dụng xe mỗi năm).

### D. Xây dựng mô hình Học máy (Machine Learning Modeling)
- **Các thuật toán Hồi quy (Regression)**: 
  - *Baseline*: Linear Regression, Ridge.
  - *Tree-based / Ensemble*: Random Forest, XGBoost, LightGBM (các thuật toán này thường hoạt động cực kỳ tốt với dạng dữ liệu bảng / tabular data).
- **Cross-validation (Xác thực chéo)**: Kỹ thuật K-Fold để đánh giá mô hình khách quan, tránh Overfitting.
- **Hyperparameter Tuning**: Dùng `RandomizedSearchCV` để tìm bộ tham số tối ưu cho mô hình.

### E. Các độ đo đánh giá (Evaluation Metrics)
- **MAE (Mean Absolute Error)**: Sai số tuyệt đối trung bình (dễ giải thích cho người thường).
- **RMSE (Root Mean Squared Error)**: Phạt nặng các dự đoán sai lệch quá lớn.
- **R² (R-squared)**: Tỉ lệ phương sai của giá được mô hình giải thích (Càng gần 1 càng tốt).
- **MAPE (Mean Absolute Percentage Error)**: Sai số tính theo phần trăm, công bằng khi so sánh sai số của xe đắt tiền và xe rẻ tiền.
*Lưu ý: Nếu huấn luyện mô hình bằng `log(price)`, phải chuyển đổi ngược (hàm `exp`) ra VNĐ trước khi tính MAE, RMSE.*

---

## 2. Định nghĩa Hoàn thành (Definition of Done - DoD)

Phần việc của Bảo sẽ được coi là **hoàn thành** khi đạt đủ các tiêu chí sau:

1. **Pipeline Notebook Hoàn Chỉnh (`model.ipynb`)**: 
   - Code chạy trơn tru từ đầu đến cuối không lỗi (Đọc dữ liệu -> EDA -> Làm sạch -> Feature Engineering -> Train -> Đánh giá).
2. **Dữ liệu sạch**:
   - Xuất ra được file `chotot_xemay_clean.csv` đã được xử lý toàn bộ nhiễu (giá ảo, xe mới, số km vô lý, thiếu dữ liệu...).
3. **Thí nghiệm "Trước và Sau"**:
   - Phải có phần so sánh kết quả độ đo của mô hình khi chạy trên dữ liệu thô (raw) và khi chạy trên dữ liệu đã làm sạch (clean) để đưa vào báo cáo.
4. **Phân tích kết quả chuyên sâu**:
   - Có biểu đồ Feature Importance (hoặc dùng SHAP) để giải thích yếu tố nào quyết định giá xe.
   - Có phân tích chi tiết từ 10-20 trường hợp mô hình dự đoán sai nhiều nhất và lý do vì sao.
5. **Đóng gói Mô hình**:
   - Mô hình tốt nhất được lưu lại dưới dạng file `.pkl`.
   - (Tùy chọn/Khuyến khích) Có app Streamlit demo nhỏ để người dùng nhập thông số xe và trả về giá dự đoán.
6. **Báo cáo và Slide**:
   - Hoàn thành Chương 3 (Khám phá và tiền xử lý) & Chương 4 (Mô hình và kết quả) trong file Báo cáo Word.
   - Chuẩn bị slide thuyết trình cho các phần tương ứng, chọn lọc 3-4 biểu đồ EDA đẹp nhất và bảng so sánh kết quả mô hình.

---

## 3. Phân tích Dữ liệu Khám phá (EDA) trên Dữ liệu Thực tế

Dựa trên file dữ liệu đã thu thập (`data/raw/chotot_xemay_named.csv`), dưới đây là những bước EDA cụ thể bạn cần thực hiện và lý do tại sao:

1. **Kiểm tra và xử lý Phân phối Biến Mục Tiêu (`price`)**:
   - *Tại sao*: Giá xe máy thường có phân phối lệch phải (right-skewed). Nhiều xe có giá vài triệu, nhưng số ít xe tay ga cao cấp (SH) có giá hàng trăm triệu. Ngoài ra, người dùng có thể nhập sai giá (giá ảo 1 tỷ, hoặc 1.000 VNĐ).
   - *Hành động*: Vẽ `histogram` cho cột `price` và một biểu đồ khác cho `log1p(price)`. Lọc bỏ các mức giá vô lý (dưới 2 triệu hoặc trên 500 triệu) và kiểm tra cờ `is_price_not_valid`.

2. **Khám phá Đặc trưng Phân loại (Categorical Features)**:
   - *Tại sao*: Dữ liệu có nhiều cột danh mục như `brand_name` (Hãng), `model_name` (Dòng xe), `type_name` (Loại xe). Giá trị xe phụ thuộc lớn vào hãng (Honda thường giữ giá tốt hơn các hãng khác).
   - *Hành động*: Vẽ `boxplot` so sánh giá xe (`price`) theo `brand_name` và `type_name`. Xem đếm tần suất (`value_counts`) để nhóm các dòng xe quá hiếm (dưới 20 tin) thành nhóm "Khác".

3. **Khám phá Đặc trưng Số (Numerical Features)**:
   - *Tại sao*: Năm đăng ký (`regdate`) và số km đã đi (`mileage_v2`) ảnh hưởng trực tiếp đến độ hao mòn và giá trị xe. Tuy nhiên, có rất nhiều dữ liệu nhiễu (số km = 0, hoặc quá cao > 500.000).
   - *Hành động*: Vẽ `scatterplot` giữa `regdate` và `price`, giữa `mileage_v2` và `price`. 

4. **Tình trạng xe (`condition_ad_name`)**:
   - *Tại sao*: Đồ án chỉ dự đoán giá xe cũ. Dữ liệu thực tế có thể lẫn tin đăng bán xe "Mới".
   - *Hành động*: Kiểm tra tần suất của `condition_ad_name` và loại bỏ các tin không phải xe "Đã sử dụng".

---

## 4. Pseudo Code / Notebook Code Mockup

Dưới đây là một đoạn code mẫu (bằng Python/Pandas/Scikit-learn/XGBoost) để giúp Bảo hình dung cách triển khai pipeline trên tập dữ liệu thực tế đã được chuẩn bị:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================================
# 1. Đọc dữ liệu
# ==========================================
# Sử dụng file có tên (named) để dễ EDA và visualize
df = pd.read_csv('data/raw/chotot_xemay_named.csv')

# ==========================================
# 2. Tiền xử lý & Làm sạch (Data Cleaning)
# ==========================================
# 2.1 Chỉ lấy xe đã sử dụng và là tin rao bán ('s' = bán)
df_clean = df[(df['condition_ad_name'] == 'Đã sử dụng') & (df['type'] == 's')].copy()

# 2.2 Lọc nhiễu giá (Chỉ giữ xe từ 2 triệu đến 500 triệu) và không bị gán cờ giá ảo
df_clean = df_clean[
    (df_clean['price'] >= 2e6) & 
    (df_clean['price'] <= 500e6) &
    (df_clean['is_price_not_valid'] == False)
]

# 2.3 Lọc nhiễu năm đăng ký & số km
df_clean = df_clean[(df_clean['regdate'] >= 1990) & (df_clean['regdate'] <= 2026)]
df_clean = df_clean[(df_clean['mileage_v2'] > 0) & (df_clean['mileage_v2'] < 500000)]

# ==========================================
# 3. Phân tích Dữ liệu Khám phá (EDA)
# ==========================================
# Vẽ phân phối giá xe
plt.figure(figsize=(10, 5))
sns.histplot(df_clean['price'], bins=50, kde=True)
plt.title('Phân phối giá xe máy (VNĐ)')
plt.show()

# Boxplot: Giá xe theo Hãng
plt.figure(figsize=(12, 6))
sns.boxplot(x='brand_name', y='price', data=df_clean)
plt.xticks(rotation=45)
plt.title('Phân bố giá xe theo Hãng (Brand)')
plt.show()

# ==========================================
# 4. Trích xuất Đặc trưng (Feature Engineering)
# ==========================================
# Tính tuổi xe (Giả sử thời điểm làm đồ án là năm 2026)
df_clean['tuoi_xe'] = 2026 - df_clean['regdate']
# Tránh chia cho 0 bằng cách thay tuổi xe 0 thành 1
df_clean['km_moi_nam'] = df_clean['mileage_v2'] / df_clean['tuoi_xe'].replace(0, 1) 

# (Tùy chọn) Extract regex từ 'subject' cho dòng xe "Dòng khác" hoặc các từ khóa

# Lựa chọn các feature để train (sử dụng mã số thay vì chuỗi cho XGBoost)
features = ['tuoi_xe', 'km_moi_nam', 'motorbikebrand', 'motorbikemodel', 'motorbikecapacity', 'region_v2']
target = 'price'

X = df_clean[features]
y = np.log1p(df_clean[target]) # Dùng log1p(price) để chuẩn hóa phân phối lệch phải

# ==========================================
# 5. Xây dựng Mô hình (Modeling)
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Khởi tạo mô hình (dùng XGBoost vì xử lý tốt dữ liệu dạng bảng)
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# ==========================================
# 6. Đánh giá Kết quả (Evaluation)
# ==========================================
y_pred_log = model.predict(X_test)
# Chuyển ngược log về VNĐ bằng expm1
y_pred = np.expm1(y_pred_log)
y_test_real = np.expm1(y_test)

print(f"MAE: {mean_absolute_error(y_test_real, y_pred):,.0f} VNĐ")
print(f"R-squared: {r2_score(y_test_real, y_pred):.4f}")
```
