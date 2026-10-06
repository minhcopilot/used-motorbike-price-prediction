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
