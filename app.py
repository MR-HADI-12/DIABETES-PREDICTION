import streamlit as st
import plotly.graph_objects as go

# ------------------ Page Settings ------------------
st.set_page_config(page_title="Diabetes Dashboard", layout="wide", page_icon="🩺")

# ------------------ CSS ------------------
st.markdown("""
<style>
body {
    color: #F8F8F8; 
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}

/* Welcome Page */
.welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 10vh;
    padding-bottom: 5rem;
    text-align: center;
    background: linear-gradient(135deg, #1C2E4A 0%, #00BFFF 50%, #ADD8E6 100%);
    background-size: cover;
}
.welcome-title {
    font-size: 3rem !important;
    font-weight: 700;
    color: #FFD700 !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.welcome-subtitle {
    font-size: 1.25rem !important;
    color: #E0F2F7 !important;
    margin-bottom: 2rem !important;
    max-width: 600px;
    font-style: italic;
}
.welcome-text {
    color: #FFFFFF !important;
    text-align: center;
    font-size: 1.1em;
    margin-bottom: 0.5rem;
}

/* Input & Button */
[data-testid="stTextInput"] > div > div > input {
    background-color: #FFFFFF;
    color: #1C2E4A;
    border: none;
    border-radius: 8px;
    padding: 12px 15px;
    font-size: 1em;
    width: 100%;
    box-sizing: border-box;
    text-align: left;
}
[data-testid="stTextInput"] {width: 100%; max-width: 300px;}
.stButton>button {
    background-color: #FFD700 !important;
    color: #1C2E4A !important;
    border-radius: 8px;
    font-weight: bold;
    padding: 12px 20px;
    font-size: 1.1em;
    border: none;
    transition: all 0.3s ease-in-out;
    width: 100%;
    max-width: 300px;
}
.stButton>button:hover {background-color: #FFC300 !important; color: #1C2E4A !important; transform: translateY(-2px);}

/* Dashboard */
[data-testid="stAppViewContainer"], .main .block-container, div.stApp {
    background: linear-gradient(135deg, #1C2E4A 0%, #00BFFF 50%, #ADD8E6 100%) !important;
    background-size: cover;
}
.dashboard-panel {
    background-color: rgba(28, 46, 74, 0.7);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
}
.about-panel {
    background-color: rgba(28, 46, 74, 0.6);
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
.about-panel h2 {color: #FFD700 !important; margin-bottom: 10px;}
.about-panel p {color: #FFFFFF; font-size: 1em; line-height: 1.5em;}
h1, h2, h3, h4, h5 {color: #FFD700 !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.4);}
.stSidebar > div:first-child {background-color: rgba(28, 46, 74, 0.8);}
.stSidebar .stSlider [data-testid="stWidgetLabel"] label { color: #FFFDD0 !important; }
.stSidebar .st-cq, .stSidebar p { color: #E0F2F7 !important; }
[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p,
[data-testid="stExpander"] ul, [data-testid="stExpander"] li,
.main .block-container strong { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# ------------------ Risk Calculation ------------------
def calculate_risk(glucose, bp, insulin, bmi, age):
    points = 0
    if glucose < 100: points += 0
    elif glucose <= 125: points += 20
    elif glucose <= 200: points += 40
    else: points += 60
    if bp < 120: points += 0
    elif bp <= 139: points += 10
    elif bp <= 159: points += 20
    else: points += 30
    if insulin < 80: points += 0
    elif insulin <= 150: points += 10
    elif insulin <= 300: points += 20
    else: points += 30
    if bmi < 25: points += 0
    elif bmi <= 29: points += 10
    elif bmi <= 34: points += 20
    else: points += 30
    if age < 35: points += 0
    elif age <= 50: points += 10
    elif age <= 65: points += 20
    else: points += 30
    risk_percent = round((points / 180) * 100, 2)
    if risk_percent >= 70: (risk_msg, risk_color) = ("⚠️ HIGH RISK","#FF3333")
    elif risk_percent >= 40: (risk_msg, risk_color) = ("⚠️ MODERATE RISK","#FF9933")
    else: (risk_msg, risk_color) = ("✅ LOW RISK","#33CC33")
    return risk_percent, risk_msg, risk_color

# ------------------ Dashboard ------------------
def show_dashboard():
    st.markdown(f"<div class='dashboard-panel'><h1>🩺 Welcome, {st.session_state.user_name.capitalize()}!</h1>", unsafe_allow_html=True)
    
    # Sidebar Inputs
    st.sidebar.header("Patient Metrics (Input Values)")
    glucose = st.sidebar.slider("Glucose Level (mg/dL)", 0, 300, 120)
    bp = st.sidebar.slider("Blood Pressure (mm Hg)", 0, 200, 70)
    insulin = st.sidebar.slider("Insulin Level (µU/mL)", 0, 900, 80)
    bmi = st.sidebar.slider("BMI", 0.0, 70.0, 25.0)
    age = st.sidebar.slider("Age", 0, 120, 30)

    # Risk Calculation
    risk_percent, risk_msg, risk_color = calculate_risk(glucose, bp, insulin, bmi, age)

    # Risk Display
    st.markdown(f"<span style='color:#FFFFFF;'>**Risk Assessment:**</span> <span style='color:{risk_color}; font-size:18px'>{risk_msg} ({risk_percent}%)</span>", unsafe_allow_html=True)
    st.caption("0–39% = Low, 40–69% = Moderate, 70%+ = High")

    # Gauge Chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percent,
        number={'suffix':'%'},
        gauge={'axis': {'range':[0,100]},
               'bar': {'color': risk_color},
               'steps': [
                   {'range':[0,40],'color':'#33CC33'},
                   {'range':[40,70],'color':'#FF9933'},
                   {'range':[70,100],'color':'#FF3333'}]}))
    fig.update_layout(height=250, paper_bgcolor="rgba(28, 46, 74, 0.7)", font_color="#F8F8F8")
    st.plotly_chart(fig, use_container_width=True)

    # Metrics Gauges
    st.markdown("### 🔧 Patient Metrics")
    cols = st.columns(5)
    metrics = {"Glucose": (glucose,70), "BP":(bp,120), "Insulin":(insulin,100), "BMI":(bmi,24.9), "Age":(age,50)}
    for col,(m,(val,norm)) in zip(cols, metrics.items()):
        col_color = "#4DA6FF" if val<=norm else "#FF66B2" if val<=norm*1.2 else "#FF0000"
        fg = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            title={'text':m},
            gauge={'axis':{'range':[0,norm*2]}, 'bar':{'color':col_color}}
        ))
        fg.update_layout(height=200, paper_bgcolor="rgba(28, 46, 74, 0.7)", font_color="#F8F8F8", margin=dict(l=1,r=1,t=15,b=2))
        col.plotly_chart(fg,use_container_width=True)

    # Recommendations Expanders
    with st.expander("💡 General Precautions", expanded=True):
        st.markdown("**Healthy Diet:** Balanced, less sugar.\n**Exercise:** 30min daily walk.\n**Monitoring:** Track glucose & BP regularly.")
    with st.expander("🏃 Suggested Exercises"):
        st.write("- Walking, jogging, cycling, yoga")
    with st.expander("💊 Typical Medications"):
        st.write("- Metformin, Sulfonylureas, Insulin if prescribed")

    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ About Panel ------------------
    st.markdown("""
    <div class="about-panel">
        <h2>✨ About This App ✨</h2>
        <p>This interactive dashboard helps you assess your potential risk of diabetes by adjusting key health metrics like Glucose, Blood Pressure, BMI, Insulin, and Age.</p>
        <p>Provides real-time feedback with clear visual gauges and recommendations to help you understand your health better.</p>
        <p><b>Designed & Developed by: Abdul Rehman (BSCS Student)</b><br>📧 ar7798768@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ Welcome Page ------------------
def show_welcome_page():
    st.markdown("""
    <div class="welcome-container">
        <h1 class="welcome-title">Your Path to Better Health</h1>
        <p class="welcome-subtitle">Use this tool to proactively assess your health metrics and understand your diabetes risk.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<p class="welcome-text">Enter your name to begin your health journey.</p>', unsafe_allow_html=True)
        user_name = st.text_input("", key="user_name_input", label_visibility="collapsed", placeholder="Your Name")
        if st.button("Start Assessment", key="start_assessment_button"):
            if user_name:
                st.session_state.name_submitted = True
                st.session_state.user_name = user_name
                st.rerun()
            else:
                st.warning("Please enter your name to continue.")

# ------------------ Main App Logic ------------------
if 'name_submitted' not in st.session_state:
    st.session_state.name_submitted = False
    st.session_state.user_name = ""

if st.session_state.name_submitted:
    show_dashboard()
else:
    show_welcome_page()
