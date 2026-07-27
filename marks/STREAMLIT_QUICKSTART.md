# Streamlit Dashboard - Quick Start Guide

## ✅ What's Been Created

### Files Created:
1. **`cardioUiDashboard.py`** - Main Streamlit application
2. **`streamlit_requirements.txt`** - Python dependencies
3. **`STREAMLIT_README.md`** - Comprehensive documentation
4. **`run_streamlit.bat`** - Quick start script for Windows

## 🚀 Quick Start (3 Easy Steps)

### Option 1: Using the Batch Script (Easiest)
```bash
# Just double-click or run:
run_streamlit.bat
```

### Option 2: Manual Start
```bash
# 1. Install dependencies (first time only)
pip install -r streamlit_requirements.txt

# 2. Run the dashboard
streamlit run cardioUiDashboard.py
```

## 🎨 Features

### Same UI as React Dashboard
- ✅ **Personal Information**: Age, Weight, Height, Gender
- ✅ **Blood Pressure**: Systolic/Diastolic BP, Cholesterol
- ✅ **Glucose Level**: Blood glucose monitoring
- ✅ **Lifestyle**: Smoking, Alcohol, Physical Activity
- ✅ **Risk Assessment**: LOW/MEDIUM/HIGH with color coding
- ✅ **Model Selection**: Random Forest or Logistic Regression
- ✅ **Visualizations**: Gauge charts, probability breakdowns

### Additional Features
- 📊 **Interactive Plotly Charts**: Beautiful, responsive visualizations
- 🎯 **Real-time Predictions**: Instant results as you input data
- 📈 **Model Comparison**: Side-by-side performance metrics
- 💡 **Helpful Tooltips**: Guidance for each input field
- 🎨 **Modern Design**: Gradient backgrounds, smooth animations

## 📁 Project Structure

```
Project ML/
├── cardioUiDashboard.py          # Main Streamlit app
├── streamlit_requirements.txt     # Dependencies
├── STREAMLIT_README.md            # Full documentation
├── run_streamlit.bat              # Quick start script
└── artifacts/                     # Model files
    ├── best_random_forest_tuned.joblib
    ├── logistic_regression.joblib
    ├── preprocessor.joblib
    └── random_forest_baseline.joblib
```

## 🔧 How It Works

### 1. Direct Model Loading
Unlike the React dashboard that uses an API server, the Streamlit version:
- Loads models directly from `artifacts/` folder
- No need for separate API server
- Faster predictions (no network overhead)

### 2. Feature Processing
```python
Input → BMI Calculation → Feature Preparation → Preprocessing → Prediction
```

The app handles:
- BMI calculation from weight/height
- Age conversion (years → days)
- All 14 required features for preprocessor
- Feature selection (6 key features for model)

### 3. Prediction Pipeline
```python
1. User inputs data
2. Calculate BMI
3. Prepare 14-column DataFrame
4. Apply preprocessor transformation
5. Model predicts using 6 key features
6. Display risk level and probabilities
```

## 🎯 Key Differences from React Dashboard

| Feature | React Dashboard | Streamlit Dashboard |
|---------|----------------|---------------------|
| **Technology** | Next.js + React | Pure Python |
| **Backend** | Separate API server | Integrated |
| **Setup** | npm install + API | pip install only |
| **Models** | Via API calls | Direct loading |
| **Speed** | Network latency | Instant |
| **Deployment** | Node.js + Python | Python only |
| **Development** | JSX + TypeScript | Python only |

## 📊 Model Information

### Models Used
- **Random Forest (Tuned)** ⭐ - Best performance
  - Accuracy: 73.2% | ROC AUC: 79.8%
  
- **Logistic Regression** - Fast & interpretable
  - Accuracy: 72.4% | ROC AUC: 78.6%

### Features Used (6 key features)
1. `ap_hi` - Systolic blood pressure
2. `ap_lo` - Diastolic blood pressure
3. `age_years` - Age in years
4. `cholesterol` - Cholesterol level (1/2/3)
5. `bmi` - Body Mass Index (calculated)
6. `weight` - Weight in kg

## 🎨 UI Components

### Input Sections
1. **Personal Information**
   - Age, Weight, Height, Gender
   - Auto-calculates BMI

2. **Blood Pressure & Cholesterol**
   - Systolic/Diastolic BP
   - Cholesterol levels (1=Normal, 2=Above, 3=Well Above)

3. **Glucose Level**
   - Blood glucose (1=Normal, 2=Above, 3=Well Above)

4. **Lifestyle Factors**
   - Smoking, Alcohol, Physical Activity

### Results Display
1. **Risk Card**
   - Color-coded (Green/Yellow/Red)
   - Risk level (LOW/MEDIUM/HIGH)
   - Prediction (Present/Absent)

2. **Metrics**
   - Model used
   - Calculated BMI
   - Confidence score

3. **Visualizations**
   - Gauge chart (0-100% risk)
   - Probability bar chart
   - Model comparison table

## 🐛 Troubleshooting

### Issue: Models not loading
**Solution**: Ensure `artifacts/` folder is in the same directory as `cardioUiDashboard.py`

### Issue: Import errors
**Solution**: Install dependencies
```bash
pip install -r streamlit_requirements.txt
```

### Issue: Wrong predictions
**Solution**: Verify you're using the correct cholesterol/glucose values:
- 1 = Normal
- 2 = Above Normal
- 3 = Well Above Normal

## 🚀 Next Steps

### To Run:
1. Open terminal in project directory
2. Run: `streamlit run cardioUiDashboard.py`
3. Dashboard opens at `http://localhost:8501`

### To Test:
Try these test cases:

**Low Risk Patient:**
- Age: 30, Weight: 65kg, Height: 170cm
- BP: 120/80, Cholesterol: 1, Glucose: 1
- No smoking, No alcohol, Active

**High Risk Patient:**
- Age: 70, Weight: 115kg, Height: 170cm
- BP: 180/80, Cholesterol: 3, Glucose: 3
- Smoking, Alcohol, Inactive

## 📝 Notes

- The Streamlit version uses the **exact same models** as the React dashboard
- All predictions should match between both dashboards
- The cholesterol/glucose fix (1/2/3 instead of 0/1/2) is already applied
- BMI is calculated automatically from weight and height

## 🎉 Advantages

1. **Simpler Setup**: No need for separate API server
2. **Pure Python**: No JavaScript knowledge required
3. **Faster Development**: Built-in components and styling
4. **Easy Deployment**: Streamlit Cloud, Docker, or any Python host
5. **Interactive**: Automatic reactivity and updates
6. **Beautiful**: Professional UI out of the box

---

**Ready to use! Just run `streamlit run cardioUiDashboard.py` or double-click `run_streamlit.bat`**
