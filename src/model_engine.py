import pandas as pd
import numpy as np

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


