# 📁 CardioML Project - Complete File Structure

## Project Root Directory
```
c:\Users\Lenovo\Downloads\Project ML\
```

## Files Overview

### 📊 Data & Models Files
- **cardio_train_properly_separated_comma.csv** - Original dataset (70,000 samples)
- **artifacts/** - Trained model files
  - preprocessor.joblib - Data preprocessing pipeline
  - best_random_forest_tuned.joblib - Best performing model
  - logistic_regression.joblib - Alternative model

### 📓 Jupyter Notebooks
- **Dataset_EDA.ipynb** - Initial exploratory data analysis
- **Project.ipynb** - Original project notebook
- **Project1.ipynb** - Updated project notebook
- **Project_Organized.ipynb** - ⭐ Main organized notebook with all tasks (34 cells executed)

### 🌐 Backend API
- **api_server.py** - Flask API server with 6 endpoints
  - /health - Health check
  - /api/predict - Single prediction
  - /api/predict/batch - Batch predictions
  - /api/models/info - Model information
  - /api/model/metrics - Detailed metrics
  - /api/feature/importance - Feature importance

### 📖 Documentation Files (Root Level)
- **UI_SETUP_GUIDE.md** - Installation and setup guide
- **UI_FEATURES_SUMMARY.md** - Complete features overview
- **PROJECT_SUMMARY.md** - ML project results summary

### 💻 Frontend Dashboard (ml-dashboard/)

#### Main Application Files
```
ml-dashboard/
├── src/
│   ├── app/
│   │   ├── layout.tsx           - Root HTML structure & metadata
│   │   └── page.tsx             - Home page entry point
│   │
│   ├── components/
│   │   ├── main-dashboard.tsx   - Container component (manages pages)
│   │   ├── navbar.tsx           - Top navigation bar (API status, settings)
│   │   ├── sidebar.tsx          - Left sidebar navigation (3 main pages)
│   │   ├── dashboard.tsx        - Legacy dashboard (replaced)
│   │   │
│   │   ├── pages/
│   │   │   ├── overview.tsx     - Dashboard page (KPIs, charts)
│   │   │   ├── prediction-form.tsx - Predictions form (health data input)
│   │   │   └── analytics.tsx    - Analytics page (learning curves, insights)
│   │   │
│   │   └── ui/
│   │       ├── button.tsx       - Custom Button component
│   │       └── card.tsx         - Custom Card component
│   │
│   ├── lib/
│   │   └── utils.ts             - Utility functions (cn class merger)
│   │
│   └── globals.css              - Global styles & Tailwind directives
│
├── Configuration Files
│   ├── package.json             - Dependencies & scripts
│   ├── tsconfig.json            - TypeScript configuration
│   ├── tailwind.config.ts       - Tailwind CSS configuration
│   ├── postcss.config.ts        - PostCSS configuration
│   ├── next.config.js           - Next.js configuration
│   └── .gitignore               - Git ignore rules
│
├── Environment Files
│   └── .env.example             - Environment variables template
│
└── Documentation
    ├── README.md                - Main project README
    └── UI_DOCUMENTATION.md      - Detailed UI guide
```

---

## 📊 File Descriptions

### **api_server.py** (200+ lines)
**Purpose**: Flask API backend for ML model predictions
**Key Features**:
- Loads 3 trained models (RF Tuned, RF Baseline, Logistic Regression)
- 6 REST endpoints for predictions and model info
- CORS enabled for frontend integration
- Error handling and logging
- Single and batch prediction support

**Main Endpoints**:
```
GET  /health
GET  /api/models/info
POST /api/predict
POST /api/predict/batch
GET  /api/model/metrics
GET  /api/feature/importance
```

### **Project_Organized.ipynb** (44 cells)
**Purpose**: Complete ML pipeline in organized format
**Key Sections**:
- Task 1-2: Data loading & EDA
- Task 3: Feature engineering
- Task 4: Model selection (3 models)
- Task 5: Model implementation
- Task 6: Training & evaluation
- Task 7: Cross-validation
- Task 8: Hyperparameter tuning
- Task 9: Visualization (6+ charts)

**All 34 code cells executed successfully**

### **main-dashboard.tsx** (Container)
**Purpose**: Main dashboard layout and routing
**Key Functions**:
- Manages active page state
- Renders navbar and sidebar
- Routes between pages (overview, predict, analytics)
- Handles sidebar toggle for mobile

### **navbar.tsx** (Professional Top Bar)
**Features**:
- Logo and branding
- API status indicator (🟢 Online)
- Notification bell with indicator
- Settings button
- User profile avatar
- Responsive menu toggle

### **sidebar.tsx** (Navigation Menu)
**Features**:
- 3 main navigation items with icons
- Active page highlighting with gradient
- Mobile responsive (collapsible)
- Settings section
- System status footer
- Logout button

### **overview.tsx** (Dashboard Page)
**Components**:
- Header section
- 4 KPI cards with gradients
- Performance comparison bar chart
- Confusion matrix pie chart
- Model details cards
- System status indicator

### **prediction-form.tsx** (Prediction Page)
**Components**:
- 5 organized form sections
- 10+ input fields (numeric and dropdown)
- Real-time API integration
- Color-coded result cards (Low/Medium/High risk)
- Confidence score with progress bar
- Model information display
- Loading and error states

### **analytics.tsx** (Analytics Page)
**Components**:
- 3 summary KPI cards
- Learning curve line chart
- Feature importance horizontal bar chart
- 5-fold cross-validation results
- Model comparison table
- 6 key insights with recommendations

### **UI Components** (ui/)
**button.tsx**: Custom Button with variants
- Variants: default, destructive, outline, secondary, ghost, link
- Sizes: default, sm, lg, icon

**card.tsx**: Card component system
- Card, CardHeader, CardTitle, CardDescription
- CardContent, CardFooter

### **globals.css** (Styling)
**Features**:
- Tailwind CSS directives
- CSS variables for theming
- Custom scrollbar styling
- Focus state styling
- Animation keyframes
- Color palette definition

---

## 🚀 Running Files

### Start Backend
```powershell
cd "c:\Users\Lenovo\Downloads\Project ML"
& "C:\Users\Lenovo\Anaconda3\python.exe" api_server.py
```
✅ Runs on http://localhost:5000

### Start Frontend
```bash
cd ml-dashboard
npm install
npm run dev
```
✅ Runs on http://localhost:3000

### Run Jupyter Notebook
```bash
# In Project_Organized.ipynb
# Run all cells in order (34 code cells)
```

---

## 📦 Dependencies

### Frontend (Node.js)
- next 14.0.0
- react 18.2.0
- react-dom 18.2.0
- recharts 2.10.0
- lucide-react 0.263.0
- tailwindcss 3.3.0
- typescript 5.0.0
- axios 1.6.0

### Backend (Python)
- flask
- flask-cors
- joblib
- numpy
- scikit-learn (for model loading)

---

## 📈 Model Files (artifacts/)

1. **preprocessor.joblib**
   - Type: ColumnTransformer + StandardScaler + OneHotEncoder
   - Purpose: Data preprocessing
   - Input: Raw patient data
   - Output: Scaled & encoded features

2. **best_random_forest_tuned.joblib**
   - Type: Random Forest Classifier
   - Performance: 73.2% Accuracy, 0.798 ROC AUC
   - Hyperparameters: n_estimators=200, max_depth=10
   - Status: ⭐ Best performing model

3. **logistic_regression.joblib**
   - Type: Logistic Regression
   - Performance: 72.4% Accuracy, 0.786 ROC AUC
   - Status: Alternative model, good generalization

---

## 🎨 Component Tree

```
MainDashboard
├── Navbar
│   ├── Logo
│   ├── Menu Toggle (mobile)
│   ├── Status Indicator
│   ├── Notifications
│   ├── Settings
│   └── User Avatar
│
├── Sidebar
│   ├── Logo Section
│   ├── Navigation Items
│   │   ├── Dashboard
│   │   ├── Predictions
│   │   └── Analytics
│   ├── Settings
│   └── Footer Status
│
└── Main Content
    ├── Overview Page
    │   ├── Header
    │   ├── 4 KPI Cards
    │   ├── Bar Chart
    │   ├── Pie Chart
    │   └── Status Card
    │
    ├── Prediction Form Page
    │   ├── Form (5 sections)
    │   ├── Input Fields
    │   ├── Submit Button
    │   └── Results Card
    │
    └── Analytics Page
        ├── Summary Cards
        ├── Line Chart
        ├── Bar Chart
        ├── CV Results
        ├── Model Comparison
        └── Insights Card
```

---

## 📊 Data Flow

```
User Input (Prediction Form)
    ↓
Form Validation
    ↓
API Call (POST /api/predict)
    ↓
Flask Backend
    ├── Load Preprocessor
    ├── Transform Features
    ├── Load Model
    ├── Make Prediction
    └── Return Results
    ↓
Parse Response
    ↓
Display Result Card
    (with risk level & confidence)
```

---

## 🔄 File Dependencies

### Frontend Dependencies
```
page.tsx
  └── main-dashboard.tsx
      ├── navbar.tsx
      │   └── button.tsx
      ├── sidebar.tsx
      │   └── button.tsx
      └── pages/
          ├── overview.tsx (Card, Button)
          ├── prediction-form.tsx (Card, Button, Charts)
          └── analytics.tsx (Card, Charts)
```

### Backend Dependencies
```
api_server.py
  ├── flask
  ├── flask_cors
  ├── joblib
  ├── numpy
  └── artifacts/
      ├── preprocessor.joblib
      ├── best_random_forest_tuned.joblib
      └── logistic_regression.joblib
```

---

## 📋 Configuration Files Purpose

| File | Purpose |
|------|---------|
| package.json | Node dependencies & npm scripts |
| tsconfig.json | TypeScript compiler options |
| tailwind.config.ts | Tailwind CSS theme & plugins |
| postcss.config.ts | CSS post-processing |
| next.config.js | Next.js framework options |
| .env.example | Environment variable template |

---

## 🎯 File Organization Summary

```
ROOT (Project ML)
├── Data Files (CSV)
├── Notebooks (Jupyter)
├── Models (ML artifacts)
├── Backend API (Python)
├── Documentation (Markdown)
└── Frontend App (Next.js)
    ├── App Shell (Next.js)
    ├── Components (React)
    ├── Styling (CSS/Tailwind)
    ├── Configuration (Config files)
    └── Documentation (UI Guide)
```

---

## ✅ All Required Files Present

- ✓ ML models trained and saved
- ✓ Jupyter notebook with complete pipeline
- ✓ Flask API server
- ✓ Next.js frontend application
- ✓ React components (navbar, sidebar, pages)
- ✓ Styling and configuration
- ✓ Complete documentation

**Status**: 🟢 All files in place, system fully operational

---

**Last Updated**: January 6, 2026  
**Total Files**: 25+  
**Project Status**: ✨ Complete & Production Ready
