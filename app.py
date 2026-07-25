import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="CustomerIQ — AI Intelligence Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -- FastAPI Backend URL --
API_URL = "http://127.0.0.1:8000/predict"

# ---------------------------------------------------------------
# DRIBBBLE UI STYLING (Custom CSS)
# ---------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #030712 !important;
    color: #F9FAFB !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

[data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"] {
    display: none !important;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(17, 24, 39, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    margin-bottom: 20px;
}

.glass-card-glow {
    background: radial-gradient(circle at top left, rgba(99, 102, 241, 0.15), transparent 60%), rgba(17, 24, 39, 0.75);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
}

/* Sliders Customization */
[data-testid="stSlider"] label {
    color: #9CA3AF !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

div[data-baseweb="slider"] div[role="slider"] {
    background: #6366F1 !important;
    border: 3px solid #FFFFFF !important;
    box-shadow: 0 0 18px #6366F1 !important;
}

/* Dribbble Style Neon Button */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 16px 0 !important;
    width: 100% !important;
    box-shadow: 0 4px 25px rgba(99, 102, 241, 0.45) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    box-shadow: 0 8px 35px rgba(168, 85, 247, 0.65) !important;
    transform: translateY(-2px) scale(1.01) !important;
}
</style>
""", unsafe_allow_html=True)

SEGMENTS = {
    "VIP": {
        "color": "#F59E0B",
        "badge_bg": "rgba(245, 158, 11, 0.15)",
        "desc": "Top-tier buyers generating maximum revenue and loyalty.",
        "action": "Trigger automated VIP invite & dedicated account manager."
    },
    "Regular": {
        "color": "#3B82F6",
        "badge_bg": "rgba(59, 130, 246, 0.15)",
        "desc": "Consistent purchasing cycle with high potential to upgrade.",
        "action": "Enroll in personalized cross-sell and bundle promotions."
    },
    "Inactive": {
        "color": "#EF4444",
        "badge_bg": "rgba(239, 68, 68, 0.15)",
        "desc": "At risk of churn. Extended period since last transaction.",
        "action": "Deploy high-value win-back discount via SMS/Email."
    },
    "New": {
        "color": "#10B981",
        "badge_bg": "rgba(16, 185, 129, 0.15)",
        "desc": "First-time buyers requiring onboarding engagement.",
        "action": "Send welcome sequence with second-purchase incentives."
    }
}

# ---------------------------------------------------------------
# HEADER / HERO UI
# ---------------------------------------------------------------
st.markdown("""
<div style="text-align: center; padding: 40px 0 20px 0;">
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 100px; padding: 6px 18px; color: #818CF8; font-size: 0.8rem; font-weight: 600; margin-bottom: 18px;">
        <span style="width: 8px; height: 8px; background: #6366F1; border-radius: 50%; box-shadow: 0 0 10px #6366F1; display: inline-block;"></span>
        NEXT-GEN CUSTOMER SEGMENTATION ENGINE
    </div>
    <h1 style="font-size: 3.2rem; font-weight: 800; color: #FFFFFF; margin: 0; line-height: 1.15; letter-spacing: -0.02em;">
        Predict Behavior. <span style="background: linear-gradient(90deg, #818CF8 0%, #C084FC 50%, #F472B6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Scale Revenue.</span>
    </h1>
    <p style="color: #9CA3AF; font-size: 1.05rem; max-width: 600px; margin: 14px auto 0 auto; line-height: 1.6;">
        Real-time K-Means Machine Learning engine analyzing behavioral telemetry to segment customer profiles instantly.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# MAIN INTERFACE (SIDE-BY-SIDE DESIGN)
# ---------------------------------------------------------------
col_input, col_output = st.columns([1.1, 1], gap="large")

with col_input:
    st.markdown("""
    <div class="glass-card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #FFF;">⚡ Behavior Input Matrix</div>
            <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #9CA3AF; font-size: 0.7rem; font-weight: 600; padding: 4px 10px; border-radius: 6px;">5 PARAMETERS</span>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        total_spent = st.slider("Total Spend (PKR)", 0, 500000, 45000, step=1000)
        total_orders = st.slider("Total Orders", 0, 200, 18, step=1)
        avg_order_value = st.slider("Avg Order Value (PKR)", 0, 50000, 2500, step=250)
    with c2:
        days_since = st.slider("Days Since Last Order", 0, 365, 12, step=1)
        rating = st.slider("Customer Satisfaction Rating", 1.0, 5.0, 4.2, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)
    predict = st.button("RUN AI PREDICTION")
    st.markdown("</div>", unsafe_allow_html=True)

with col_output:
    if not predict:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 50px 28px;">
            <div style="width: 56px; height: 56px; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px auto; color: #818CF8; font-size: 1.5rem;">
                ✦
            </div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">Awaiting Prediction Stream</div>
            <p style="color: #6B7280; font-size: 0.88rem; max-width: 320px; margin: 0 auto; line-height: 1.5;">
                Adjust behavioral signals on the left panel and execute AI classification.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        payload = {
            "total_spent": total_spent,
            "total_orders": total_orders,
            "avg_order_value": avg_order_value,
            "days_since": days_since,
            "rating": rating
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            result = response.json()
            segment = result["segment"]
            cluster = result["cluster"]
            seg = SEGMENTS[segment]

            st.markdown(f"""
            <div class="glass-card-glow">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
                    <div>
                        <div style="color: {seg['color']}; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px;">SYSTEM CLASSIFICATION</div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">{segment}</div>
                    </div>
                    <div style="background: {seg['badge_bg']}; border: 1px solid {seg['color']}88; color: {seg['color']}; padding: 8px 18px; border-radius: 100px; font-weight: 700; font-size: 0.85rem;">
                        CLUSTER #{cluster}
                    </div>
                </div>
                
                <p style="color: #D1D5DB; font-size: 0.95rem; line-height: 1.6; margin-bottom: 24px;">
                    {seg['desc']}
                </p>

                <div style="background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px;">
                    <div style="color: #818CF8; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                        RECOMMENDED ACTION
                    </div>
                    <div style="color: #F3F4F6; font-size: 0.9rem; font-weight: 500;">
                        {seg['action']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Backend Offline: Terminal me 'uvicorn main:app --reload' run karein.")
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------------------------------------------------------
# SEGMENT CARDS GUIDE
# ---------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #4B5563; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;'>CLUSTER DIRECTORY</div>", unsafe_allow_html=True)

g1, g2, g3, g4 = st.columns(4)
cols = [g1, g2, g3, g4]

for idx, (seg_name, seg) in enumerate(SEGMENTS.items()):
    with cols[idx]:
        st.markdown(f"""
        <div style="background: rgba(17, 24, 39, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 18px;">
            <div style="color: {seg['color']}; font-weight: 800; font-size: 1rem; margin-bottom: 4px;">{seg_name}</div>
            <div style="color: #6B7280; font-size: 0.78rem; line-height: 1.4;">{seg['desc']}</div>
        </div>
        """, unsafe_allow_html=True)