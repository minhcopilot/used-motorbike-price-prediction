# Project Checklist & Expected Issues

## 1. Data Cleaning Issues (To be handled by Bảo)
Based on the data collected on 05/10/2026, the following data issues (noise) must be addressed:
- [ ] **Invalid Prices**: 115 records have prices < 2 million VND (including 0 VND) and 44 records have prices > 500 million VND (fake prices).
- [ ] **Wrong Condition**: 462 records are for "New" bikes. The model only targets used motorbikes.
- [ ] **Invalid Mileage**: 780 records have 0 km, 333 records have > 500,000 km, and ~1.4% are missing mileage entirely.
- [ ] **Invalid Registration Year**: 3 records have registration year = 0 or < 1980. Some years might conflict with the title.
- [ ] **Missing Features**: 58% missing origin, 51% missing engine capacity.
- [ ] **Generic Model Names**: 1,835 records are labeled as "Dòng khác" (Other models). Needs regex to extract the actual model from the title (`subject`).
- [ ] **Buying vs Selling**: Ensure posts with `type = 'k'` (cần mua/want to buy) are filtered out, keeping only `type = 's'` (bán/sell).
- [ ] **Duplicate Records**: Check and remove any re-posted duplicates using `list_id` or combinations of (title, price, year, km).

## 2. Feature Engineering Tasks
- [ ] Calculate `tuoi_xe` (Age of bike) = 2026 - `regdate`.
- [ ] Calculate `km_moi_nam` (Km per year) = `mileage` / `tuoi_xe`.
- [ ] Apply `log(price)` transformation due to right-skewed distribution.
- [ ] Group rare motorbike models (< 20 listings) into a "Khác" (Other) category.
- [ ] Extract flag features from the title (e.g., "chính chủ", "biển số đẹp", "zin").
- [ ] Apply One-hot Encoding or Target Encoding for categorical variables.

## 3. Modeling & Evaluation Tasks
- [ ] Split data 80/20 for Train/Test and use 5-fold Cross-validation.
- [ ] Train and compare 4 models: Linear Regression (baseline), Ridge, Random Forest, XGBoost/LightGBM.
- [ ] Perform Hyperparameter Tuning using `RandomizedSearchCV`.
- [ ] Conduct "Before vs. After Cleaning" experiment to demonstrate the value of data cleaning.
- [ ] Analyze feature importance (or SHAP) and error cases (e.g., top 10-20 worst predictions).

## 4. Deliverables Checklist
- [ ] `chotot_xemay_clean.csv` (Cleaned dataset)
- [ ] `model.ipynb` (End-to-end reproducible notebook)
- [ ] Saved model file (`.pkl`)
- [ ] (Optional) Streamlit Demo App
- [ ] Report Chapters 3 & 4 (EDA, Preprocessing, Modeling, Results)
- [ ] Presentation slides for EDA and Modeling parts
