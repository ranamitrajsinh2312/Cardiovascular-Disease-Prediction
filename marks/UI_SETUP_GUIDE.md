# 🚀 Complete ML Project UI Setup Guide

## Project Overview

You now have a **complete Machine Learning application** with:
- ✅ **Frontend**: Modern Next.js + Shadcn/ui dashboard
- ✅ **Backend**: Flask API server for predictions
- ✅ **ML Models**: Trained models in artifacts folder
- ✅ **Database Ready**: Ready for PostgreSQL/MongoDB integration

---

## 📁 Directory Structure

```
Project ML/
├── cardio_train_properly_separated_comma.csv
├── Dataset_EDA.ipynb
├── Project_Organized.ipynb          # Main ML notebook
├── PROJECT_SUMMARY.md               # Project summary
├── api_server.py                    # Flask API server
├── artifacts/
│   ├── preprocessor.joblib
│   ├── best_random_forest_tuned.joblib
│   └── logistic_regression.joblib
└── ml-dashboard/                    # React Next.js frontend
    ├── src/
    │   ├── app/
    │   ├── components/
    │   ├── lib/
    │   └── globals.css
    ├── package.json
    ├── tailwind.config.ts
    ├── next.config.ts
    ├── tsconfig.json
    └── README.md
```

---

## 🔧 Installation & Setup

### Step 1: Backend API Setup

```bash
# Navigate to project directory
cd "c:\Users\Lenovo\Downloads\Project ML"

# Install Flask dependencies
pip install flask flask-cors joblib numpy

# Run the API server
python api_server.py
```

**Expected Output:**
```
🚀 Starting ML Cardio API Server...
🌐 Server running on http://localhost:5000
```

### Step 2: Frontend Dashboard Setup

```bash
# Navigate to dashboard directory
cd ml-dashboard

# Install Node.js dependencies (if not already done)
npm install

# Run development server
npm run dev
```

**Expected Output:**
```
> next dev
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## 📊 Accessing the Application

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend Dashboard** | http://localhost:3000 | View models, make predictions |
| **API Server** | http://localhost:5000 | Backend API endpoints |
| **Health Check** | http://localhost:5000/health | Verify API is running |
| **Model Info** | http://localhost:5000/api/models/info | Get model details |

---

## 🎯 Dashboard Features

### 1. **Overview Tab**
- Model Performance Comparison (Bar Chart)
- Confusion Matrix (Pie Chart)  
- Feature Importance (Horizontal Bar Chart)

### 2. **Metrics Tab**
- Detailed metrics for each model
- Accuracy, Precision, Recall, F1, ROC AUC
- Cross-validation stability info

### 3. **Predictions Tab**
- Input form for patient health data
- Real-time prediction results
- Risk level classification (Low/Medium/High)
- Confidence scores

### 4. **Analysis Tab**
- Model performance summary
- Key insights & warnings
- Production deployment recommendations

---

## 🔌 API Endpoints

### Health Check
```bash
GET http://localhost:5000/health
```

### Get Model Information
```bash
GET http://localhost:5000/api/models/info
```

### Single Prediction
```bash
POST http://localhost:5000/api/predict
Content-Type: application/json

{
  "model": "random_forest",
  "features": {
    "age_years": 45,
    "weight": 70,
    "height": 170,
    "cholesterol": 1,
    "gluc": 1,
    "ap_hi": 120,
    "ap_lo": 80
  }
}
```

### Batch Predictions
```bash
POST http://localhost:5000/api/predict/batch
Content-Type: application/json

{
  "samples": [
    {"age_years": 45, "weight": 70, ...},
    {"age_years": 50, "weight": 75, ...}
  ]
}
```

### Get Model Metrics
```bash
GET http://localhost:5000/api/model/metrics
```

### Get Feature Importance
```bash
GET http://localhost:5000/api/feature/importance
```

---

## 🔗 Frontend-Backend Integration

The dashboard is ready to connect to the API. Update the API base URL:

**In `ml-dashboard/src/components/dashboard.tsx`:**

```typescript
const API_BASE_URL = 'http://localhost:5000'

const handlePrediction = async (features) => {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'random_forest',
      features: features
    })
  })
  const result = await response.json()
  console.log('Prediction:', result)
}
```

---

## 📦 Technology Stack

### Frontend
- **Next.js 14** - React Framework
- **Shadcn/ui** - Professional UI Components
- **Tailwind CSS** - Utility-first CSS
- **Recharts** - Data Visualization
- **TypeScript** - Type Safety

### Backend
- **Flask** - Python Web Framework
- **Flask-CORS** - Cross-Origin Support
- **Joblib** - Model Serialization
- **NumPy** - Numerical Computing

### ML Models
- **scikit-learn** - Machine Learning Library
- **Logistic Regression** - Baseline Model
- **Random Forest** - Ensemble Model (Best)

---

## 🚀 Production Deployment

### Frontend Deployment (Vercel - Recommended)
```bash
cd ml-dashboard
npm install -g vercel
vercel
```

### Backend Deployment (Heroku/Railway/Render)

**Heroku Example:**
```bash
heroku create ml-cardio-api
git push heroku main
heroku logs --tail
```

**Create `requirements.txt`:**
```bash
pip freeze > requirements.txt
```

**Create `Procfile`:**
```
web: gunicorn api_server:app
```

### Docker Deployment (Optional)

**Create `Dockerfile`:**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "api_server:app", "-b", "0.0.0.0:5000"]
```

---

## 🎨 Customization

### Change Dashboard Colors
Edit `ml-dashboard/src/globals.css`:
```css
--primary: 222.2 47.6% 11.2%;
--secondary: 210 40% 96%;
--accent: 222.2 47.6% 11.2%;
```

### Add New API Endpoints
Edit `api_server.py`:
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    return jsonify({'result': 'data'})
```

### Add New Dashboard Tabs
Edit `ml-dashboard/src/components/dashboard.tsx`:
```typescript
{['overview', 'metrics', 'predictions', 'analysis', 'new-tab'].map(...)}
```

---

## 📊 Performance Metrics Reference

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
|-------|----------|-----------|--------|----------|---------|
| **RF Tuned** ⭐ | 73.2% | 75.7% | 68.3% | 71.8% | **0.798** |
| LR | 72.4% | 74.6% | 67.8% | 71.1% | 0.786 |
| RF Baseline | 72.1% | 73.2% | 69.7% | 71.4% | 0.783 |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Frontend - use different port
cd ml-dashboard && npm run dev -- -p 3001

# Backend - use different port
python api_server.py  # Change port 5000 in code
```

### CORS Issues
Make sure Flask has CORS enabled in `api_server.py`:
```python
from flask_cors import CORS
CORS(app)
```

### Models Not Loading
Verify artifacts path:
```python
import os
print(os.path.exists('artifacts/best_random_forest_tuned.joblib'))
```

### Dependencies Issues
```bash
# Frontend
cd ml-dashboard && rm -rf node_modules package-lock.json && npm install

# Backend
pip install --upgrade flask flask-cors joblib
```

---

## ✅ Next Steps

- [ ] Connect prediction form to API
- [ ] Add authentication (JWT/OAuth)
- [ ] Implement database (PostgreSQL/MongoDB)
- [ ] Add prediction history
- [ ] Real-time model monitoring
- [ ] User feedback mechanism
- [ ] Model retraining pipeline
- [ ] Containerize with Docker
- [ ] Deploy to cloud platform
- [ ] Set up CI/CD pipeline

---

## 📚 Documentation Files

- **README.md** (in ml-dashboard/) - Detailed setup guide
- **PROJECT_SUMMARY.md** - ML project summary
- **api_server.py** - API documentation in docstrings
- **This file** - Complete integration guide

---

## 🤝 Support & Resources

- **Next.js**: https://nextjs.org/docs
- **Shadcn/ui**: https://ui.shadcn.com
- **Tailwind CSS**: https://tailwindcss.com
- **Flask**: https://flask.palletsprojects.com
- **Recharts**: https://recharts.org

---

## ✨ Project Status

- ✅ ML Models Trained & Tuned
- ✅ Frontend Dashboard Built  
- ✅ API Server Created
- ✅ Integration Ready
- ⏳ Production Deployment (Next Step)

**Last Updated**: January 6, 2026  
**Status**: Ready for Development & Deployment 🚀
