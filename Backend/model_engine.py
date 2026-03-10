import pandas as pd
import numpy as np

def get_data_insights():
    try:
        df = pd.read_csv('cleaned_placement_data.csv')

    except FileNotFoundError:
        df = pd.read_csv('student_placement_prediction_dataset_2026.csv')
        
    avg_cgpa = df['cgpa'].mean()
    placed_df = df[df['placement_status'] == 'Placed']
    avg_salary = placed_df['salary_package_lpa'].mean()
    
    return df.head(10), avg_cgpa, avg_salary



def predict_placement(data_dict):

    coding_pts = data_dict['coding_score'] * 0.30

    aptitude_pts = data_dict['aptitude_score'] * 0.25 
    
    intern_pts = min(data_dict['internships'], 5) * 4
    
    project_pts = min(data_dict['projects'], 5) * 3
    
    cgpa_pts = data_dict['cgpa'] * 1.0

    total_score = coding_pts + aptitude_pts + intern_pts + project_pts + cgpa_pts
    

    if data_dict['backlogs'] > 0:
        total_score -= (data_dict['backlogs'] * 15)

    if total_score >= 70:
        status = "Placed"
        coding_bonus = (data_dict['coding_score'] - 50) * 0.1
        est_salary = 5.0 + coding_bonus + (total_score - 70) * 0.2
    else:
        status = "Not Placed"
        est_salary = 0.0
        
    return status, round(est_salary, 2)


#skill upgrader

def load_data_from_csv(file_path):
    """Loads the dataset and cleans up column names."""
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]
    return df

def filter_dataframe(df, target_company, target_role):
    """Filters the dataframe based on user selections."""
    filtered_df = df.copy()
    if target_company != "All":
        filtered_df = filtered_df[filtered_df['Company'] == target_company]
    if target_role != "All":
        filtered_df = filtered_df[filtered_df['Job Role'] == target_role]
    return filtered_df

def analyze_gap(required_skills_str, user_skills_list):
    """Calculates match score and missing skills for a single row."""
    if pd.isna(required_skills_str):
        return "0%", ""

    # Convert string of skills from CSV into a list
    req_skills = [s.strip().lower() for s in str(required_skills_str).split(",")]
    
    # Calculate matches and missing
    matched = [s for s in req_skills if s in user_skills_list]
    missing = [s for s in req_skills if s not in user_skills_list]
    
    score = (len(matched) / len(req_skills)) * 100 if req_skills else 0
    return f"{score:.0f}%", ", ".join(missing)

def calculate_skill_gaps(df, user_skills_list):
    """Applies the gap analysis to the entire dataframe."""
    if df.empty:
        return df
    
    # Apply the analysis function and create new columns
    results = df.apply(lambda row: analyze_gap(row['Skills Needed'], user_skills_list), axis=1)
    df['Match Score'], df['Skills to Learn'] = zip(*results)
    return df


