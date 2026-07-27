"""
Cardio Disease Prediction Dashboard - Streamlit Version
Uses the trained ML models from artifacts folder
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="CardioML - Disease Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-card {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .low-risk {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
    }
    .medium-risk {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
    }
    .high-risk {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #dc3545;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Load models
@st.cache_resource
def load_models():
    """Load the trained models and preprocessor.

    Includes a small compatibility shim for older LogisticRegression
    artifacts that might be missing the ``multi_class`` attribute when
    loaded with a newer scikit-learn version.
    """
    base_dir = Path(__file__).parent
    artifacts_dir = base_dir / "artifacts"
    
    try:
        preprocessor = joblib.load(artifacts_dir / "preprocessor.joblib")
        rf_model = joblib.load(artifacts_dir / "best_random_forest_tuned.joblib")
        lr_model = joblib.load(artifacts_dir / "logistic_regression.joblib")

        # Patch legacy LogisticRegression models if needed
        try:
            from sklearn.linear_model import LogisticRegression  # type: ignore

            if isinstance(lr_model, LogisticRegression) and not hasattr(lr_model, "multi_class"):
                try:
                    default_multi_class = LogisticRegression().multi_class
                except Exception:
                    default_multi_class = "ovr"
                setattr(lr_model, "multi_class", default_multi_class)
        except Exception:
            # If scikit-learn is not available or anything goes wrong,
            # continue without patching and let Streamlit surface errors.
            pass
        
        return {
            'preprocessor': preprocessor,
            'random_forest': rf_model,
            'logistic_regression': lr_model,
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def calculate_bmi(weight, height_cm):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def prepare_features(form_data):
    """Prepare features for prediction"""
    # Calculate BMI
    bmi = calculate_bmi(form_data['weight'], form_data['height'])
    
    # Convert age to days (as the preprocessor expects)
    age_in_days = form_data['age_years'] * 365
    
    # Create DataFrame with all required columns
    feature_data = {
        'id': [1],
        'age': [age_in_days],
        'age_years': [form_data['age_years']],
        'gender': [form_data['gender']],
        'height': [form_data['height']],
        'weight': [form_data['weight']],
        'ap_hi': [form_data['ap_hi']],
        'ap_lo': [form_data['ap_lo']],
        'cholesterol': [form_data['cholesterol']],
        'gluc': [form_data['gluc']],
        'smoke': [form_data['smoke']],
        'alco': [form_data['alco']],
        'active': [form_data['active']],
        'cardio': [0]  # Dummy target
    }
    
    return pd.DataFrame(feature_data), bmi

def get_risk_level(probability):
    """Determine risk level from probability"""
    if probability > 0.7:
        return "HIGH", "high-risk"
    elif probability > 0.4:
        return "MEDIUM", "medium-risk"
    else:
        return "LOW", "low-risk"

def create_gauge_chart(probability, risk_level):
    """Create a gauge chart for risk visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Disease Risk: {risk_level}", 'font': {'size': 24}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#d4edda'},
                {'range': [40, 70], 'color': '#fff3cd'},
                {'range': [70, 100], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">❤️ CardioML - Disease Prediction Dashboard</h1>', unsafe_allow_html=True)
    
    # Load models
    models = load_models()
    
    if models['status'] == 'error':
        st.error(f"❌ Error loading models: {models['message']}")
        st.info("Please ensure the artifacts folder contains the required .joblib files")
        return
    
    st.success("✅ Models loaded successfully!")
    
    # Sidebar for model selection
    with st.sidebar:
        st.header("⚙️ Settings")
        model_choice = st.selectbox(
            "Select Model",
            ["Random Forest (Tuned)", "Logistic Regression"],
            help="Choose the prediction model"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Model Performance")
        if model_choice == "Random Forest (Tuned)":
            st.metric("Accuracy", "73.2%")
            st.metric("ROC AUC", "79.8%")
            st.metric("Precision", "75.7%")
            st.metric("Recall", "68.3%")
        else:
            st.metric("Accuracy", "72.4%")
            st.metric("ROC AUC", "78.6%")
            st.metric("Precision", "74.6%")
            st.metric("Recall", "67.8%")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Patient Health Data")
        
        # Personal Information
        st.subheader("👤 Personal Information")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            age_years = st.number_input("Age (years)", min_value=18, max_value=80, value=45, step=1)
        with col_b:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
        with col_c:
            height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170, step=1)
        
        gender = st.selectbox("Gender", options=[1, 2], format_func=lambda x: "Female" if x == 1 else "Male")
        
        # Blood Pressure & Cholesterol
        st.subheader("🩺 Blood Pressure & Cholesterol")
        col_d, col_e, col_f = st.columns(3)
        
        with col_d:
            ap_hi = st.number_input("Systolic BP (ap_hi)", min_value=80, max_value=200, value=120, step=1)
        with col_e:
            ap_lo = st.number_input("Diastolic BP (ap_lo)", min_value=40, max_value=130, value=80, step=1)
        with col_f:
            cholesterol = st.selectbox(
                "Cholesterol Level",
                options=[1, 2, 3],
                format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[x]
            )
        
        # Glucose Level
        st.subheader("🍬 Glucose Level")
        gluc = st.selectbox(
            "Blood Glucose Level",
            options=[1, 2, 3],
            format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[x]
        )
        
        # Lifestyle Factors
        st.subheader("🏃 Lifestyle Factors")
        col_g, col_h, col_i = st.columns(3)
        
        with col_g:
            smoke = st.selectbox("Smoking", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        with col_h:
            alco = st.selectbox("Alcohol", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        with col_i:
            active = st.selectbox("Physical Activity", options=[0, 1], format_func=lambda x: "Inactive" if x == 0 else "Active")
        
        # Predict button
        st.markdown("---")
        predict_button = st.button("🔮 Get Prediction", use_container_width=True)
    
    with col2:
        st.header("📊 Prediction Results")
        
        if predict_button:
            # Prepare form data
            form_data = {
                'age_years': age_years,
                'weight': weight,
                'height': height,
                'gender': gender,
                'ap_hi': ap_hi,
                'ap_lo': ap_lo,
                'cholesterol': cholesterol,
                'gluc': gluc,
                'smoke': smoke,
                'alco': alco,
                'active': active
            }
            
            # Prepare features
            feature_df, bmi = prepare_features(form_data)
            
            # Preprocess
            features_processed = models['preprocessor'].transform(feature_df)
            
            # Make prediction
            if model_choice == "Random Forest (Tuned)":
                prediction = models['random_forest'].predict(features_processed)[0]
                probability = models['random_forest'].predict_proba(features_processed)[0]
            else:
                prediction = models['logistic_regression'].predict(features_processed)[0]
                probability = models['logistic_regression'].predict_proba(features_processed)[0]
            
            # Get risk level
            disease_prob = probability[1]
            risk_level, risk_class = get_risk_level(disease_prob)
            
            # Display results
            st.markdown(f"""
            <div class="risk-card {risk_class}">
                <h2>{risk_level} RISK</h2>
                <h3>{'Disease Present' if prediction == 1 else 'Disease Absent'}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            st.markdown(f"""
            <div class="metric-card">
                <h4>Model Used</h4>
                <p style="font-size: 1.2rem;">{model_choice}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>Calculated BMI</h4>
                <p style="font-size: 1.2rem;">{bmi:.1f} kg/m²</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>Confidence Score</h4>
                <p style="font-size: 1.2rem;">{max(probability) * 100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Gauge chart
            st.plotly_chart(create_gauge_chart(disease_prob, risk_level), use_container_width=True)
            
            # Probability breakdown
            st.markdown("### 📈 Probability Breakdown")
            prob_df = pd.DataFrame({
                'Outcome': ['No Disease', 'Disease Present'],
                'Probability': [probability[0] * 100, probability[1] * 100]
            })
            
            fig = px.bar(
                prob_df,
                x='Outcome',
                y='Probability',
                color='Outcome',
                color_discrete_map={'No Disease': '#28a745', 'Disease Present': '#dc3545'},
                text='Probability'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=300,
                yaxis_title="Probability (%)",
                xaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Model comparison table
    if predict_button:
        st.markdown("---")
        st.header("📊 Model Comparison (Reference)")
        
        comparison_data = {
            'Model': ['RF Tuned ⭐', 'RF Baseline', 'Logistic Regression'],
            'Accuracy': ['73.2%', '72.1%', '72.4%'],
            'Precision': ['75.7%', '73.2%', '74.6%'],
            'Recall': ['68.3%', '69.7%', '67.8%'],
            'F1 Score': ['71.8%', '71.4%', '71.1%'],
            'ROC AUC': ['79.8%', '78.3%', '78.6%']
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
