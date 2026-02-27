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
   