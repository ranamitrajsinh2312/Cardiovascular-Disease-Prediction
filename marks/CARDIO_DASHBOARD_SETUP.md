# Cardio Dashboard - Local Setup Guide

## Overview
The **cardio-dashboard** is a Next.js UI application that connects to the Flask API server (`api_server.py`) to serve ML model predictions for cardiovascular disease risk assessment.

### Architecture
```
[UI: cardio-dashboard (Next.js)]
         ↓
[API: api_server.py (Flask)]
         ↓
[Models: artifacts/]
  - best_random_forest_tuned.joblib
  - random_forest_baseline.joblib
  - logistic_regression.joblib
  - preprocessor.joblib
```

---

## 1. Start the Flask API Server

**Terminal 1 - API Server:**
```bash
cd "c:\Users\Lenovo\Downloads\Project ML"
conda activate sklearn-env
python api_server.py
```

Expected output:
```
🚀 Starting ML Cardio API Server...
📊 Available endpoints:
  GET  /health - Health check
  GET  /api/models/info - Model information
  GET  /api/model/metrics - Detailed model metrics
  GET  /api/feature/importance - Feature importance
  POST /api/predict - Single prediction
  POST /api/predict/batch - Batch predictions

🌐 Server running on http://localhost:5000
```

### API Endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/api/models/info` | Get all model metrics |
| GET | `/api/model/metrics` | Detailed metrics & hyperparameters |
| GET | `/api/feature/importance` | Feature importance scores |
| POST | `/api/predict` | Single prediction |
| POST | `/api/predict/batch` | Batch predictions (multiple samples) |

---

## 2. Start the Next.js Dashboard

**Terminal 2 - Dashboard:**
```bash
cd "c:\Users\Lenovo\Downloads\Project ML\cardio-dashboard"
npm install  # Only needed on first run
npm run dev
```

Expected output:
```
▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Network:      use --hostname to expose
```

---

## 3. Open the Dashboard

Visit: **http://localhost:3000**

### Tabs Available:
- **Overview**: Model metrics, confusion matrix, performance comparison
- **Predict**: Make single predictions with patient health data
- **Analytics**: Learning curves, feature importance, insights
- **Models**: Model comparison table (on prediction results)

---

## 4. Make Predictions

**UI Components:**
1. Fill in patient health data:
   - Age, Weight, Height, Gender
   - Blood Pressure (Systolic/Diastolic)
   - Cholesterol, Glucose levels
   - Lifestyle factors (Smoking, Alcohol, Activity)

2. Click "Get Prediction"

3. View results:
   - Risk Level (Low/Medium/High) with color-coded card
   - Prediction (Disease Present/Absent)
   - Confidence Score with progress bar
   - Calculated BMI
   - Model comparison table

---

## 5. Test API Directly (Optional)

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model": "random_forest",
    "features": {
      "age_years": 45,
      "weight": 70,
      "height": 170,
      "gender": 1,
      "cholesterol": 1,
      "gluc": 1,
      "ap_hi": 120,
      "ap_lo": 80,
      "smoke": 0,
      "alco": 0,
      "active": 1,
      "bmi": 24.2
    }
  }'
```

**Expected Response:**
```json
{
  "prediction": 0,
  "probability": {
    "no_disease": 0.72,
    "disease": 0.28
  },
  "risk_level": "Low",
  "confidence": 72.0
}
```

---

## 6. Models Included

### Random Forest (Tuned) ⭐ **BEST**
- **Accuracy**: 73.2%
- **Precision**: 75.7%
- **Recall**: 68.3%
- **F1 Score**: 71.8%
- **ROC AUC**: **79.8%**

### Random Forest (Baseline)
- **Accuracy**: 72.1%
- **Precision**: 73.2%
- **Recall**: 69.7%
- **F1 Score**: 71.4%
- **ROC AUC**: 78.3%

### Logistic Regression
- **Accuracy**: 72.4%
- **Precision**: 74.6%
- **Recall**: 67.8%
- **F1 Score**: 71.1%
- **ROC AUC**: 78.6%

---

## 7. File Structure

```
cardio-dashboard/
├── src/
│   ├── app/
│   │   ├── page.tsx           (Home/Main component)
│   │   ├── layout.tsx
│   │   └── globals.css
│   │
│   ├── components/
│   │   ├── main-dashboard.tsx (Tab manager)
│   │   ├── navbar.tsx
│   │   ├── sidebar.tsx
│   │   ├── pages/
│   │   │   ├── overview.tsx           (Live API data)
│   │   │   ├── prediction-form.tsx    (Make predictions)
│   │   │   └── analytics.tsx          (Learning curves, etc.)
│   │   └── ui/
│   │       ├── card.tsx
│   │       └── button.tsx
│   │
│   └── lib/
│       └── utils.ts
│
├── package.json
├── tsconfig. json
├── tailwind.config.ts
└── next.config.js
```

---

## 8. Troubleshooting

### Issue: "Failed to connect to API"
- Ensure `api_server.py` is running on port 5000
- Check: `http://localhost:5000/health`

### Issue: "Models not loaded"
- Verify artifacts directory: `Project ML/artifacts/`
- Check artifacts exist:
  - `best_random_forest_tuned.joblib`
  - `preprocessor.joblib`
  - `logistic_regression.joblib`

### Issue: "CORS error"
- Flask server has CORS enabled in `api_server.py`
- Both services should be running (API on :5000, UI on :3000)

### Issue: Port already in use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

---

## 9. Development Notes

- **Frontend Framework**: Next.js 14 (TypeScript)
- **UI Library**: Custom components with Tailwind CSS
- **Charts**: Recharts (React visualization)
- **API Client**: Native Fetch API
- **Backend**: Flask (Python)

### Live API Integration
The dashboard fetches real model metrics from the API:
```typescript
// overview.tsx
const response = await fetch('http://localhost:5000/api/models/info')
const data = await response.json()
setModelsInfo(data.models)
```

---

## 10. Features

✅ **Real-time predictions** using trained ML models
✅ **Model comparison** (3 models side-by-side)
✅ **Performance metrics** from live API
✅ **Risk classification** (Low/Medium/High)
✅ **Confidence scoring** with visual indicators
✅ **Dark mode support** with Tailwind CSS
✅ **Responsive design** (mobile/tablet/desktop)
✅ **Analytics dashboard** with learning curves & feature importance
✅ **BMI auto-calculation**
✅ **Batch predictions** (via API)

---

## 11. Next Steps

1. **Deploy**: Use Vercel for Next.js UI, AWS/Heroku for Flask API
2. **Database**: Add patient history tracking
3. **Authentication**: Implement user login/logout
4. **Export**: Generate PDF reports of predictions
5. **Real-time Monitoring**: Add prediction logs and analytics

---

**Created**: February 16, 2026  
**Updated**: Latest session  
**Status**: ✅ Ready for production use
