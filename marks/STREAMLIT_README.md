# CardioML Streamlit Dashboard

A beautiful, interactive Streamlit dashboard for cardiovascular disease prediction using trained ML models.

## Features

- 🎨 **Modern UI**: Clean, professional interface with gradient backgrounds and smooth animations
- 📊 **Interactive Visualizations**: Real-time gauge charts and probability breakdowns using Plotly
- 🤖 **Multiple Models**: Choose between Random Forest (Tuned) and Logistic Regression models
- 📈 **Live Predictions**: Instant predictions with confidence scores and risk levels
- 💡 **User-Friendly**: Intuitive form inputs with helpful tooltips and validation
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Installation

### 1. Install Dependencies

```bash
pip install -r streamlit_requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas numpy joblib plotly scikit-learn
```

### 2. Verify Model Files

Ensure the `artifacts` folder contains these files:
- `best_random_forest_tuned.joblib`
- `logistic_regression.joblib`
- `preprocessor.joblib`
- `random_forest_baseline.joblib` (optional)

## Running the Dashboard

### Option 1: Using Streamlit CLI

```bash
streamlit run cardioUiDashboard.py
```

### Option 2: Using Python

```bash
python -m streamlit run cardioUiDashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## Usage Guide

### 1. Enter Patient Information

**Personal Information:**
- Age (18-80 years)
- Weight (30-150 kg)
- Height (120-220 cm)
- Gender (Female/Male)

**Blood Pressure & Cholesterol:**
- Systolic BP (80-200 mmHg)
- Diastolic BP (40-130 mmHg)
- Cholesterol Level (Normal/Above Normal/Well Above Normal)

**Glucose Level:**
- Blood Glucose (Normal/Above Normal/Well Above Normal)

**Lifestyle Factors:**
- Smoking (Yes/No)
- Alcohol Consumption (Yes/No)
- Physical Activity (Active/Inactive)

### 2. Select Model

Choose between:
- **Random Forest (Tuned)** - Best performance (79.8% ROC AUC)
- **Logistic Regression** - Fast and interpretable (78.6% ROC AUC)

### 3. Get Prediction

Click the "🔮 Get Prediction" button to:
- View risk level (LOW/MEDIUM/HIGH)
- See disease prediction (Present/Absent)
- Check confidence score
- View probability breakdown
- Compare model performance

## Understanding the Results

### Risk Levels

- **LOW RISK** (Green): Disease probability < 40%
  - Indicates low likelihood of cardiovascular disease
  
- **MEDIUM RISK** (Yellow): Disease probability 40-70%
  - Suggests moderate risk, lifestyle changes recommended
  
- **HIGH RISK** (Red): Disease probability > 70%
  - Indicates high likelihood, medical consultation advised

### Metrics Explained

- **BMI (Body Mass Index)**: Calculated from weight and height
  - Normal: 18.5-24.9
  - Overweight: 25-29.9
  - Obese: ≥30

- **Confidence Score**: Model's certainty in its prediction
  - Higher percentage = more confident prediction

- **Probability Breakdown**: Shows likelihood of each outcome
  - Helps understand the model's decision-making

## Model Performance

### Random Forest (Tuned) ⭐
- **Accuracy**: 73.2%
- **ROC AUC**: 79.8%
- **Precision**: 75.7%
- **Recall**: 68.3%
- **F1 Score**: 71.8%

### Logistic Regression
- **Accuracy**: 72.4%
- **ROC AUC**: 78.6%
- **Precision**: 74.6%
- **Recall**: 67.8%
- **F1 Score**: 71.1%

## Features & Customization

### Sidebar Settings
- Model selection
- Real-time performance metrics
- Easy switching between models

### Main Dashboard
- Organized input sections
- Clear visual hierarchy
- Responsive layout

### Results Panel
- Color-coded risk levels
- Interactive gauge chart
- Detailed probability visualization
- Model comparison table

## Technical Details

### Data Processing
1. **BMI Calculation**: weight (kg) / (height (m))²
2. **Age Conversion**: years → days (for preprocessor compatibility)
3. **Feature Engineering**: All 14 required features prepared
4. **Preprocessing**: StandardScaler + OneHotEncoder applied
5. **Prediction**: 6 key features used (ap_hi, ap_lo, age_years, cholesterol, bmi, weight)

### Model Pipeline
```
Input Data → Feature Preparation → Preprocessing → Model Prediction → Risk Assessment
```

## Troubleshooting

### Models Not Loading
- Verify `artifacts` folder exists in the same directory
- Check that all .joblib files are present
- Ensure scikit-learn version compatibility

### Import Errors
- Install all required packages: `pip install -r streamlit_requirements.txt`
- Verify Python version ≥ 3.8

### Prediction Errors
- Ensure all input values are within valid ranges
- Check that preprocessor.joblib matches the model version

## Comparison with React Dashboard

### Similarities
- ✅ Same prediction logic
- ✅ Same model files
- ✅ Same feature engineering
- ✅ Same risk level thresholds
- ✅ Similar UI layout

### Advantages of Streamlit Version
- 🚀 Faster development and deployment
- 🎨 Built-in theming and styling
- 📊 Native Plotly integration
- 🔄 Automatic reactivity
- 🐍 Pure Python (no JavaScript needed)

## Next Steps

### Enhancements
- [ ] Add batch prediction from CSV
- [ ] Export prediction reports
- [ ] Historical prediction tracking
- [ ] Model explainability (SHAP values)
- [ ] Custom risk thresholds
- [ ] Multi-language support

### Deployment Options
- **Streamlit Cloud**: Free hosting for public apps
- **Docker**: Containerized deployment
- **Heroku**: Cloud platform deployment
- **AWS/GCP/Azure**: Enterprise cloud hosting

## License

This dashboard uses the trained models from the CardioML project.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure model files are in the correct location

---

**Made with ❤️ using Streamlit**
