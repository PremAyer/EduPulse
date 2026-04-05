import pandas as pd
import os
from dotenv import load_dotenv
from src.career_engine import CareerRecommender
from src.GenAi_feedback import get_feedback_from_llm
from src.predictor import PlacementPredictor
import src.Supabase as db
import re
import streamlit as st
import random
from src.email_service import send_otp_email

# Load environment variables
load_dotenv("config/.env")

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EduPulse | Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def init_db():
    db.create_usertable()
    return True

init_db()

# --- HELPER: LIVE SYSTEM METRICS ---

# --- HELPER: LIVE SYSTEM METRICS ---
@st.cache_data(ttl=3600)
def get_live_metrics():
    # A list of places the file might be hiding
    possible_paths = [
        "Dataset_company_job roles.csv",             # If it's in the same folder
        "data/Dataset_company_job roles.csv",        # If you put it in a 'data' folder
        "src/Dataset_company_job roles.csv",         # If you put it in the 'src' folder
    ]
    
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path
            break
            
    if found_path:
        # We found it! Let's do the math.
        df = pd.read_csv(found_path)
        companies_count = len(df['Company'].unique())
        roles_count = len(df['Job Role'].unique())
        
        all_skills = set()
        for skills_str in df['Skills Needed'].dropna():
            skills = [s.strip().lower() for s in str(skills_str).split(',')]
            all_skills.update(skills)
            
        return companies_count, roles_count, len(all_skills)
    else:
        # It still couldn't find it. Let's warn the developer.
        st.sidebar.error("⚠️ Telemetry Error: Could not locate 'Dataset_company_job roles.csv'.")
        return 0, 0, 0

# --- ENTERPRISE CSS INJECTION ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* Card Styling with Hover Effects */
        .module-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .module-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,123,255,0.15);
            border-color: #007bff;
        }
        .module-card h3 {
            color: #1f1f1f !important;  
            font-weight: 700;
            margin-bottom: 10px;
        }
        .module-card p {
            color: #666666 !important;  
            font-size: 14px;
        }
        
        /* Make buttons fill the width nicely */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        /* Soften the divider */
        hr {
            margin-top: 2rem;
            margin-bottom: 2rem;
            opacity: 0.3;
        }
        </style>
        """, unsafe_allow_html=True)

# --- FUNCTION FOR THE MAIN DASHBOARD ---
def display_dashboard():
    inject_custom_css()
    
    if 'active_module' not in st.session_state:
        st.session_state['active_module'] = "Home"

    # --- SIDEBAR BRANDING ---
    with st.sidebar:
        st.markdown("### 🎓 EduPulse")
        st.caption("Department of Computer Science • AIML")
        st.divider()
        
        # Simulated User Profile
        st.markdown("👤 **Current Session**")
        st.caption("🟢 Status: Authenticated")
        st.write("")
        
        # Navigation
        st.markdown("**Navigation**")
        if st.button("🏠 Workspace Home", use_container_width=True, type="secondary" if st.session_state['active_module'] != "Home" else "primary"):
            st.session_state['active_module'] = "Home"
            st.rerun()
            
        st.divider()
        st.button("🚪 Secure Logout", on_click=lambda: st.session_state.update({"logged_in": False}), type="secondary")


    # --- VIEW 1: MAIN MENU (HOME) ---
    if st.session_state['active_module'] == "Home":
        st.title("Central Analytics Workspace")
        st.markdown("<p style='font-size: 16px; color: #666;'>Welcome to your executive dashboard. Monitor platform health, access predictive modules, and map industry skills below.</p>", unsafe_allow_html=True)
        
        # REALISTIC FEATURE: Live System Metrics
        st.markdown("#### 📈 Live Platform Telemetry")
        
        # Fetch actual data from your dataset
        companies_count, roles_count, skills_count = get_live_metrics()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="System Status", value="Operational", delta="Latency: < 50ms", delta_color="inverse")
        m2.metric(label="Companies Indexed", value=f"{companies_count}", delta="Live DB Sync", delta_color="normal")
        m3.metric(label="Career Paths Mapped", value=f"{roles_count}", delta="Industry Aligned", delta_color="off")
        m4.metric(label="Unique Skills Tracked", value=f"{skills_count}", delta="Auto-extracted", delta_color="normal")
        
        st.divider()
        st.markdown("#### 🚀 Active Modules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="module-card"><h3>📊 CDC Portal</h3><p>Placement likelihood & salary estimation engine powered by historical placement data.</p></div>', unsafe_allow_html=True)
            if st.button("Launch CDC Module", use_container_width=True):
                st.session_state['active_module'] = "CDC"
                st.rerun()

        with col2:
            st.markdown('<div class="module-card"><h3>📈 Skill Upgrader</h3><p>NLP-driven career pathing. Map your current stack against real-world tech company requirements.</p></div>', unsafe_allow_html=True)
            if st.button("Launch Skill Upgrader", use_container_width=True):
                st.session_state['active_module'] = "Success"
                st.rerun()

    # --- VIEW 2: CDC MODULE ---
    elif st.session_state['active_module'] == "CDC":
        st.title("📊 Placement Forecasting Engine")
        st.markdown("""
        **Career Development Cell (CDC) Analytics Module** This engine leverages historical placement data and predictive modeling to evaluate student profiles. It estimates the likelihood of campus placement and forecasts expected salary brackets based on core competencies.
        """)
        
        st.info("💡 **Tip:** In Manual Mode, try tweaking your Coding and Aptitude scores to see how skill improvements directly impact your estimated salary package!")
        
        predictor = PlacementPredictor()

        # Use a container for the input controls
        with st.container(border=True):
            analysis_mode = st.radio("Select Input Method:", ["Manual Entry (Single Student)", "Bulk Upload (Excel/CSV)"], horizontal=True)
        
        st.write("")

        if analysis_mode == "Manual Entry (Single Student)":
            st.sidebar.header("📝 Profile Configuration")
            inputs = {
                'coding_skill_score': st.sidebar.slider("Coding Skill Score (0-100)", 0, 100, 70),
                'aptitude_score': st.sidebar.slider("Aptitude Score (0-100)", 0, 100, 65),
                'internships_count': st.sidebar.number_input("Internships Completed", 0, 5, 1),
                'projects_count': st.sidebar.number_input("Major Projects Completed", 0, 10, 2),
                'cgpa': st.sidebar.slider("Current CGPA", 0.0, 10.0, 7.5, step=0.1),
                'backlogs': st.sidebar.number_input("Active Backlogs", min_value=0, max_value=10, value=0), 
            }

            st.subheader("Engine Output")
            if st.button("Execute Prediction Request", type="primary"):
                status, salary = predictor.predict(inputs)
                
                if status == "Placed":
                    st.markdown(f"""
                        <div style="background-color: rgba(52, 168, 83, 0.1); padding: 25px; border-left: 6px solid #34a853; border-radius: 8px; margin-bottom: 20px;">
                            <h3 style="color: #188038; margin-top: 0;">✅ Placement Probability: High</h3>
                            <p style="color: #188038; font-size: 16px; margin-bottom: 0;">Profile qualifies for <strong>Tier-1 Premium Placements</strong>.</p>
                            <h2 style="color: #188038; margin-top: 10px; margin-bottom: 0;">Estimated Package: {salary} LPA</h2>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Prediction Status: {status} - Profile requires optimization.")

                # AI Feedback
                if os.getenv("GOOGLE_API_KEY"):
                    with st.spinner("Connecting to Generative AI Core..."):
                        try:
                            feedback = get_feedback_from_llm(inputs, status, salary)
                            if status == "Placed":
                                st.subheader("🎊 AI Counselor Analysis")
                                st.success(feedback)
                            else:
                                st.subheader("💡 AI Optimization Strategy")
                                st.warning(feedback)
                        except Exception as e:
                            st.error(f"AI System Error: {e}")

        else:
            st.subheader("📁 Batch Processing Engine")
            st.write("Upload a dataset to run high-throughput placement predictions.")
            uploaded_file = st.file_uploader("Upload Student Data (CSV or Excel)", type=['csv', 'xlsx'])

            if uploaded_file:
                if uploaded_file.name.endswith('.csv'):
                    bulk_df = pd.read_csv(uploaded_file)
                else:
                    bulk_df = pd.read_excel(uploaded_file)

                with st.expander("Preview Ingested Data"):
                    st.dataframe(bulk_df.head(), use_container_width=True)

                required_cols = ['coding_skill_score', 'aptitude_score', 'internships_count', 'projects_count', 'cgpa', 'backlogs']
                missing_cols = [c for c in required_cols if c not in bulk_df.columns]

                if missing_cols:
                    st.error(f"Schema Validation Failed. Missing columns: {missing_cols}")
                else:
                    if st.button("Initialize Batch Analysis", type="primary"):
                        results = []
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        for index, row in bulk_df.iterrows():
                            student_input = {col: row[col] for col in required_cols}
                            status, salary = predictor.predict(student_input)
                            results.append({"Prediction": status, "Estimated_Salary": salary})
                            
                            progress_bar.progress((index + 1) / len(bulk_df))
                            status_text.text(f"Processing record {index + 1} of {len(bulk_df)}...")

                        res_df = pd.concat([bulk_df, pd.DataFrame(results)], axis=1)
                        status_text.empty()

                        placed_df = res_df[res_df['Prediction'] == 'Placed'].reset_index(drop=True)
                        placed_df.index = placed_df.index + 1
                        placed_df.index.name = 'S.No.'
                        
                        st.success("✅ Batch processing completed successfully.")
                    
                        
                        # Handle the edge case where no one is placed
                        if placed_df.empty:
                            st.warning("No students met the criteria for placement in this batch.")
                        else:
                            st.write(f"🎉 Found **{len(placed_df)}** Placed students:")
                            
                            # Display and download only the filtered dataframe
                            st.dataframe(placed_df, width="stretch")

                            csv = placed_df.to_csv(index=True).encode('utf-8')
                            st.download_button(
                                "📥 Export Placed Students (CSV)", 
                                data=csv, 
                                file_name="EduPulse_Placed_Students.csv", 
                                mime="text/csv"
                            )


                        
    # --- VIEW 3: SUCCESS MODULE ---
    elif st.session_state['active_module'] == "Success":
        st.title("🚀 Industry Role & Skill Gap Recommender")
        st.markdown("""
        **Bridge the gap between your current tech stack and industry standards.** Our internal NLP engine evaluates your known skills against real-world job requirements from top-tier tech companies. It predicts the role you are most naturally suited for and generates a precise roadmap of the skills you need to acquire.
        """)
        
        try:
            recommender = CareerRecommender()  
        except FileNotFoundError:
            st.error("⚠️ System Database Offline: 'Dataset_company_job roles.csv' not found.")
            st.stop()

        with st.container(border=True):
            st.subheader("🛠 Technical Profile Input")
            user_skills_input = st.text_area(
                "Declare your current technical proficiencies (comma-separated):", 
                placeholder="e.g., Python, SQL, Docker, AWS, React"
            )
            
            analyze_btn = st.button("Run Profile Analysis", type="primary")
            
        if analyze_btn:
            if not user_skills_input.strip():
                st.warning("Input required to process request.")
            else:
                with st.spinner("Processing via NLP Classification Model..."):
                    predicted_role, confidence = recommender.predict_role(user_skills_input)
                    company_analysis_df = recommender.analyze_company_fit(predicted_role, user_skills_input)

                st.markdown("---")
                st.subheader("🎯 System Prediction")
                
                # Use clean metric cards for the result
                c1, c2, c3 = st.columns([1,1,2])
                c1.metric("Optimal Role", predicted_role)
                c2.metric("Model Confidence", f"{confidence}%")
                
                if confidence > 70:
                    st.success(f"High profile alignment detected for **{predicted_role}** architecture.")
                else:
                    st.warning(f"Profile leans toward **{predicted_role}**, but significant upskilling is required for competitive advantage.")

                st.markdown(f"### 🏢 Corporate Compatibility Matrix ({predicted_role})")
                
                if company_analysis_df.empty:
                    st.info("Insufficient market data for this specific role configuration.")
                else:
                    st.dataframe(
                        company_analysis_df,
                        column_config={
                            "Formatted Score": st.column_config.ProgressColumn(
                                "Match Quotient",
                                help="Algorithmic compatibility score",
                                format="%f%%",
                                min_value=0, max_value=100,
                            ),
                            "Skills to Learn": st.column_config.TextColumn("Deficit Analysis (Required Upskilling)")
                        },
                        use_container_width=True,
                        hide_index=True
                    )


# --- MAIN APP LOGIC (LOGIN / REGISTRATION) ---
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        # Center the login panel cleanly
        _, col, _ = st.columns([1, 1.5, 1])
        with col:
            st.write("") # Spacer
            st.write("") 
            
            # Adapted Hero Section for universal theme compatibility
            st.markdown("<h1 style='text-align: center;'>🎓 EduPulse System</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 18px;'>AI-Powered Career & Placement Analytics</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 14px; opacity: 0.6; margin-bottom: 20px;'>Authenticate to access your workspace.</p>", unsafe_allow_html=True)
            
            # Use Streamlit's native container border to make the login box look like a card
            with st.container(border=True):
                tab_login, tab_signup, tab_forgot = st.tabs(["🔐 Login", "📝 Register", "🔑 Reset"])

                with tab_login:
                    st.write("") # Spacer
                    email = st.text_input("Corporate / Institutional Email", key="l_email", placeholder="user@domain.com")
                    password = st.text_input("Passphrase", type='password', key="l_pass")
                    
                    if st.button("Authenticate Session", use_container_width=True, type="primary"):
                        hashed_pswd = db.make_hashes(password)
                        result = db.login_user(email, hashed_pswd)
                        if result:
                            st.session_state['logged_in'] = True
                            st.rerun()
                        else:
                            st.error("Authentication Failed: Invalid credentials.")

                with tab_signup:
                    st.write("")
                    new_user = st.text_input("Institutional Email", key="s_email", placeholder="student@gmail.com")
                    new_password = st.text_input("Create Passphrase", type='password', key="s_pass")

                    if st.button("Provision Account", use_container_width=True):
                            if new_user.strip() == "" or new_password.strip() == "":
                                st.warning("All fields are required for provisioning.")
                            elif not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", new_user):
                                st.error("Policy Violation: Must use a valid Gmail address.")
                            else:
                                try:
                                    db.add_userdata(new_user, db.make_hashes(new_password))
                                    st.success("Account provisioned. Proceed to the Login tab.")
                                except Exception as e:
                                    if "already exists" in str(e).lower() or "unique violation" in str(e).lower():
                                        st.info("Identity already exists in registry.")
                                    else:
                                        st.error(f"System Error: {e}")

                with tab_forgot:
                    st.write("")
                    
                    # Initialize session states for the password reset flow
                    if 'reset_stage' not in st.session_state:
                        st.session_state['reset_stage'] = 'request'

                    # STAGE 1: Ask for Email
                    if st.session_state['reset_stage'] == 'request':
                        email_to_reset = st.text_input("Registered Email Address", key="f_email")
                        
                        if st.button("Send Recovery Token", use_container_width=True):
                            if not email_to_reset.strip():
                                st.warning("Please enter your email address.")
                            else:
                                with st.spinner("Generating secure token and contacting email servers..."):
                                    # Generate a random 6-digit code
                                    otp = str(random.randint(100000, 999999))
                                    
                                    # Send the email
                                    email_sent = send_otp_email(email_to_reset, otp)
                                    
                                    if email_sent:
                                        # Save the email and OTP in memory to check later
                                        st.session_state['reset_email'] = email_to_reset
                                        st.session_state['valid_otp'] = otp
                                        st.session_state['reset_stage'] = 'verify'
                                        st.rerun()
                                    else:
                                        st.error("System Error: Unable to send email. Contact Administrator.")

                    # STAGE 2: Verify OTP and Reset
                    elif st.session_state['reset_stage'] == 'verify':
                        st.info(f"📧 Recovery token dispatched to **{st.session_state['reset_email']}**")
                        
                        entered_otp = st.text_input("Enter 6-Digit Recovery Token", max_chars=6)
                        new_password = st.text_input("Create New Passphrase", type="password")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Confirm Reset", use_container_width=True, type="primary"):
                                if entered_otp == st.session_state['valid_otp']:
                                    if len(new_password) < 4:
                                        st.warning("Password too short.")
                                    else:
                                        # Hash new password and update database
                                        new_hashed = db.make_hashes(new_password)
                                        success = db.update_password(st.session_state['reset_email'], new_hashed)
                                        
                                        if success:
                                            st.success("✅ Password successfully updated. Please return to the Login tab.")
                                            # Reset the stage so the form goes back to normal
                                            st.session_state['reset_stage'] = 'request'
                                        else:
                                            st.error("Database Error: Could not update password.")
                                else:
                                    st.error("❌ Invalid Recovery Token. Please try again.")
                                    
                        with col2:
                            if st.button("Cancel", use_container_width=True):
                                st.session_state['reset_stage'] = 'request'
                                st.rerun()
                        
            st.markdown("<p style='text-align: center; font-size: 12px; opacity: 0.4; margin-top: 20px;'>Protected by EduPulse Security infrastructure.</p>", unsafe_allow_html=True)
    else:
        display_dashboard()

if __name__ == '__main__':
    main()