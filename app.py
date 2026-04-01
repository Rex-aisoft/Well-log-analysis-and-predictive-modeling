# app.py
import streamlit as st
import requests

# Set the page configuration for a wider layout and custom title
st.set_page_config(
    page_title="Integrated Well Log Assessment",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for a Geoscience aesthetic (Earth tones)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2e7b32; /* Deep forest green */
        color: white;
        border-radius: 5px;
        width: 100%;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        color: #d32f2f; /* Deep red for high visibility of target */
    }
    </style>
""", unsafe_allow_html=True)

# Main UI Header
st.title("🌍 Subsurface Predictive Modelling")
st.subheader("Deep Resistivity (RESD) Prediction Dashboard")
st.markdown("Adjust the petrophysical parameters in the sidebar to simulate different geological facies and predict formation resistivity.")

# Sidebar for Inputs
st.sidebar.header("Log Parameters")
st.sidebar.markdown("---")

    
# Using the exact industry ranges from the data cleaning step
cali = st.sidebar.number_input(
    "Caliper - CALI (in)", 
    min_value=6.0, 
    max_value=20.0, 
    value=8.5
    )
dt = st.sidebar.number_input(
    "Sonic - DT (µs/ft)", 
    min_value=40.0, 
    max_value=240.0, 
    value=100.0
    )
gr = st.sidebar.number_input(
    "Gamma Ray - GR (API)", 
    min_value=0.0, 
    max_value=150.0, 
    value=60.0)
lls = st.sidebar.number_input(
    "Shallow Resistivity - LLS (ohm.m)", 
    value=10.0
    )
nphi = st.sidebar.number_input(
    "Neutron Porosity - NPHI (v/v)", 
    min_value=-0.15, 
    max_value=0.45, 
    value=0.20
    )
rhob = st.sidebar.number_input(
    "Bulk Density - RHOB (g/cm³)", 
    min_value=1.95, 
    max_value=2.95, 
    value=2.25
    )
dept = st.sidebar.number_input(
    "Depth - DEPT (m)", 
    value=5000.0, 
    step=10.0
    )

# Main Panel layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Execute Prediction")
    predict_button = st.button("Predict RESD")

with col2:
    if predict_button:
        # Prepare the payload to match the FastAPI schema
        payload = {
            "CALI": cali,
            "DT": dt, 
            "GR": gr,
            "LLS": lls, 
            "NPHI": nphi,
            "RHOB": rhob,
            "DEPT": dept, 
        }
        
        # Send POST request to FastAPI backend
        try:
            with st.spinner("Computing formation properties..."):
                # Ensure the URL matches FastAPI server (default is usually port 8000)
                response = requests.post("http://localhost:8000/predict", json=payload)
                
            if response.status_code == 200:
                result = response.json()
                resd_value = result["predicted_RESD"]
                
                # Display the metric
                st.metric(label="Predicted RESD", value=f"{resd_value:.2f} ohm.m")
                
                # Dynamic Geologic Interpretation based on the result
                st.markdown("### Rapid Geological Insight")
                if resd_value > 50 and gr < 60:
                    st.success("**Potential Pay Zone:** High resistivity combined with low Gamma Ray indicates a clean, fluid-bearing reservoir, likely hydrocarbons.")
                elif resd_value < 10 and gr < 60:
                    st.info("**Water-Bearing Sand:** Low resistivity in a clean formation suggests brine saturation.")
                elif gr >= 60:
                    st.warning("**Non-Reservoir/Shale:** The high Gamma Ray indicates a clay-rich facies. The resistivity is likely driven by bound water or tight compaction.")
            else:
                st.error(f"API Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Could not connect to the backend. Please ensure the FastAPI server is running on localhost:8000.")