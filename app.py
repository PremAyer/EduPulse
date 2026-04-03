import pandas as pd
import os
from dotenv import load_dotenv
from src.model_engine import load_data_from_csv, filter_dataframe, calculate_skill_gaps, analyze_gap
from src.GenAi_feedback import get_feedback_from_llm
from src.predictor import PlacementPredictor
import src.Supabase as db
import re
import streamlit as st

# Load environment variables
load_dotenv("config/.env")

st.set_page_config(
    page_title="EduPulse | Student Analytics",
    page_icon="🎓",
    layout="wide"
)

@st.cache_resource
def init_db():
    db.create_usertable()
    return True

init_db()

# --- FUNCTION FOR THE MAIN DASHBOARD ---
def display_dashboard():
    
    if 'active_module' not in st.session_state:
        st.session_state['active_module'] = "Home"

    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    st.markdown("""
        <style>
        .module-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #007bff;
            text-align: center;
            margin-bottom: 10px;
        }
                
        .module-card h3 {
            color: #1f1f1f !important;  
            font-weight: bold;
        }
        .module-card p {
            color: #4f4f4f !important;  
        }
                
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- VIEW 1: MAIN MENU (HOME) ---
    if st.session_state['active_module'] == "Home":
        st.title("🎓 EduPulse Central Portal")
        st.write("Welcome! Please select a module to begin analysis.")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="module-card"><h3>📊 CDC Portal</h3><p>Placement & Salary Prediction Engine</p></div>', unsafe_allow_html=True)
            if st.button("Open CDC Module"):
                st.session_state['active_module'] = "CDC"
                st.rerun()

        with col2:
            st.markdown('<div class="module-card"><h3>📈 Skill Upgrader</h3><p>Job Role Essentials</p></div>', unsafe_allow_html=True)
            if st.button("Open Skill Upgrader Module"):
                st.session_state['active_module'] = "Success"
                st.rerun()

    # --- VIEW 2: CDC MODULE (DASHBOARD) ---
    elif st.session_state['active_module'] == "CDC":
       
        if st.sidebar.button("← Back to Menu"):
            st.session_state['active_module'] = "Home"
            st.rerun()

        # DYNAMIC SIDEBAR
        st.sidebar.header("📝 CDC Input Panel")
        inputs = {
            'coding_skill_score': st.sidebar.slider("Coding Skill Score (0-100)", 0, 100, 70),
            'aptitude_score': st.sidebar.slider("Aptitude Score (0-100)", 0, 100, 65),
            'internships_count': st.sidebar.number_input("Internships Completed", 0, 5, 1),
            'projects_count': st.sidebar.number_input("Major Projects Completed", 0, 10, 2),
            'cgpa': st.sidebar.slider("Current CGPA", 0.0, 10.0, 7.5, step=0.1),
            'backlogs': st.sidebar.number_input("Active Backlogs", min_value=0, max_value=10, value=0), 
        }

        st.title("📊 Career Development Cell (CDC)")
        st.markdown("Module: **Placement & Salary Predictor**")
        predictor = PlacementPredictor()  

        # DELETED THE COLUMN CODE HERE. JUST WRITE DIRECTLY TO THE PAGE!
        st.subheader("Prediction Engine")
        if st.button("Generate Prediction", type="primary"):
            # 1. Get ML Prediction
            status, salary = predictor.predict(inputs)
            
            
            if status == "Placed":
                    # Custom CSS for a professional "Offer" card
                    st.markdown(f"""
                        <div style="
                            background-color: #e6f4ea; 
                            padding: 20px; 
                            border-left: 10px solid #34a853; 
                            border-radius: 10px;
                            margin-bottom: 20px;">
                            <h2 style="color: #188038; margin: 0;">Placement Confirmed</h2>
                            <p style="color: #188038; font-size: 18px;">Based on your current profile, you are eligible for 
                            <strong>Tier-1 Premium Placements</strong> with an estimated package of 
                            <span style="font-size: 24px;">{salary} LPA</span>.</p>
                        </div>
                    """, unsafe_allow_html=True)
    
            else:
                st.error(f"❌ Status: {status}")
            
            # 2. Generate LLM Feedback
            st.divider()
            
            if not os.getenv("GOOGLE_API_KEY"):
                st.subheader("🤖 AI Insights")
                st.warning("⚠️ Google API key not found. Please add it to your .env file to see AI insights.")
            else:
                with st.spinner("Analyzing profile with AI..."):
                    try:
                        feedback = get_feedback_from_llm(inputs, status, salary)
                        
                        # --- DYNAMIC HEADING LOGIC ---
                        if status == "Placed":
                            st.subheader("🎊 LLM Best Wishes")
                            st.info(feedback)
                        else:
                            st.subheader("💡 LLM Important Advices")
                            st.warning(feedback)
                            
                    except Exception as e:
                        st.subheader("🤖 AI Insights")
                        st.error(f"An error occurred while fetching AI insights: {e}")
                    

    # --- VIEW 3: SUCCESS MODULE (SKILL UPGRADER) ---
    elif st.session_state['active_module'] == "Success":
        if st.sidebar.button("← Back to Menu"):
            st.session_state['active_module'] = "Home"
            st.rerun()
            
        st.title("Skill Gap Analysis")
        st.write("Analyze the gap between your current skills and industry requirements.")
        
        def load_data():
            file_path = "Dataset_company_job roles.csv" 
            try:
                return load_data_from_csv(file_path)
            except FileNotFoundError:
                st.error(f"Error: The file '{file_path}' was not found. Please check the filename in your folder.")
                return pd.DataFrame()

        df = load_data()

        if df.empty:
            st.stop()

        st.sidebar.header("Filter Options")
        target_company = st.sidebar.selectbox("Select Target Company", ["All"] + list(df['Company'].unique()))
        target_role = st.sidebar.selectbox("Select Target Role", ["All"] + list(df['Job Role'].unique()))

        st.subheader("🛠 Your Skill Profile")
        user_skills_input = st.text_input("Enter your current skills (separated by commas):", "Python, SQL, Excel")
        user_skills = [s.strip().lower() for s in user_skills_input.split(",")]

        filtered_df = filter_dataframe(df, target_company, target_role)
        analyzed_df = calculate_skill_gaps(filtered_df, user_skills)

        if not analyzed_df.empty:
            st.subheader("📈 Opportunities & Skill Gaps")
            st.dataframe(
                analyzed_df[['Company', 'Job Role', 'Skills Needed', 'Match Score', 'Skills to Learn']],
                use_container_width=True,
                hide_index=True
            )
            
            if target_role != "All":
                st.divider()
                st.subheader(f"Advice for {target_role} Role")
                all_needed = analyzed_df['Skills to Learn'].iloc[0]
                if all_needed:
                    st.info(f"To become a competitive candidate for this role, focus on learning: **{all_needed}**")
                else:
                    st.success("You have all the required skills for this role! Ready to apply!")
        else:
            st.warning("No matching roles found for the selected filters.")

# --- MAIN APP LOGIC ---
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.title("🎓 EduPulse Portal")
            tab_login, tab_signup, tab_forgot = st.tabs(["Login", "Create Account", "Forgot Password"])

            with tab_login:
                st.subheader("Login Section")
                email = st.text_input("Gmail", key="l_email")
                password = st.text_input("Password", type='password', key="l_pass")
                if st.button("Login", use_container_width=True):
                    hashed_pswd = db.make_hashes(password)
                    result = db.login_user(email, hashed_pswd)
                    if result:
                        st.session_state['logged_in'] = True
                        st.rerun()
                    else:
                        st.error("Invalid Gmail or Password")

            with tab_signup:
                st.subheader("Create New Account")
                new_user = st.text_input("Gmail", key="s_email", placeholder="example@gmail.com")
                new_password = st.text_input("Password", type='password', key="s_pass")

                if st.button("Signup", use_container_width=True):
                        if new_user.strip() == "" or new_password.strip() == "":
                            st.warning("Please enter both a Username and a Password.")
                        
                        elif not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", new_user):
                            st.error("Please enter a valid Gmail address (e.g., name@gmail.com).")

                        else:
                            try:
                                db.add_userdata(new_user, db.make_hashes(new_password))
                                st.success("Account created successfully! You can now switch to the Login tab.")
                            except Exception as e:
                                if "already exists" in str(e).lower() or "unique violation" in str(e).lower():
                                    st.info("This Gmail is already registered. Please go to the Login tab to sign in.")
                                else:
                                    st.error(f"An unexpected error occurred: {e}")

            with tab_forgot:
                st.subheader("Reset Password")
                email_to_reset = st.text_input("Enter registered Gmail", key="f_email")
                if st.button("Send Reset Link", use_container_width=True):
                    st.info(f"Reset logic triggered for {email_to_reset}")
    else:
        display_dashboard()

if __name__ == '__main__':
    main()