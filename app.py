import streamlit as st
from model_engine import get_data_insights, predict_placement
import auth_db as db
import re


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
            color: #1f1f1f !important;  /* Dark Grey for Heading */
            font-weight: bold;
        }
        .module-card p {
            color: #4f4f4f !important;  /* Medium Grey for Description */
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

        # DYNAMIC SIDEBAR (Only created when CDC is active)
        st.sidebar.header("📝 CDC Input Panel")
        inputs = {
            'cgpa': st.sidebar.slider("Current CGPA", 0.0, 10.0, 7.5, step=0.1),
            'backlogs': st.sidebar.number_input("Active Backlogs", min_value=0, max_value=10, value=0),
            'coding_score': st.sidebar.slider("Coding Skill Score (0-100)", 0, 100, 70),
            'aptitude_score': st.sidebar.slider("Aptitude Score (0-100)", 0, 100, 65),
            'internships': st.sidebar.number_input("Internships Completed", 0, 5, 1),
            'projects': st.sidebar.number_input("Major Projects Completed", 0, 10, 2)
        }

        st.title("📊 Career Development Cell (CDC)")
        st.markdown("Module: **Placement & Salary Predictor**")

        sample_df, avg_cgpa, avg_salary = get_data_insights()
        col_pred, col_bench = st.columns([1, 1.5], gap="large")

        with col_pred:
            st.subheader("Prediction Engine")
            if st.button("Generate Prediction", type="primary"):
                status, salary = predict_placement(inputs)
                if status == "Placed":
                    st.success(f"✅ Status: {status}")
                    st.metric(label="Estimated Salary Package", value=f"{salary} LPA")
                    st.balloons()
                else:
                    st.error(f"❌ Status: {status}")
        
        with col_bench:
            st.subheader("📊 Batch Benchmarks")
            m1, m2 = st.columns(2)
            m1.metric("Dataset Avg CGPA", f"{avg_cgpa:.2f}")
            m2.metric("Dataset Avg Salary", f"{avg_salary:.2f} LPA")
            st.markdown("---")
            st.dataframe(sample_df, use_container_width=True)

    # --- VIEW 3: SUCCESS MODULE ---
    elif st.session_state['active_module'] == "Success":
        if st.sidebar.button("← Back to Menu"):
            st.session_state['active_module'] = "Home"
            st.rerun()
            
        st.title("Skill Gap Analysis")
        st.info("This section is currently under development.")

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



  