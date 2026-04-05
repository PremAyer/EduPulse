import pandas as pd
import joblib

class StudentPredictor:
    def __init__(self):
        try:
            self.model = joblib.load('models/student_performance_model.pkl')

            self.features = [
                'previous_semester_sgpa', 
                'Attendance marks', 
                'assignment_score_average(out of 20)',
                'midterm_exam_avg', 
                'Lowest midterm_exam_score'
            ]

        except FileNotFoundError:
            self.model = None
        
    def predict_performance(self, df):
        if self.model is None:
            return None, "Model not found. Please run train_student_model.py first."
        
        results_df = df.copy()
        
        # Check if the uploaded CSV has the right columns
        missing_cols = [col for col in self.features if col not in df.columns]
        if missing_cols:
            return None, f"Data Error! The uploaded CSV is missing: {', '.join(missing_cols)}"
            
        X = df[self.features]
        
        try:
            # Generate Predictions
            predictions = self.model.predict(X)
            
            # 1. Insert the prediction as the very FIRST column
            results_df.insert(0, 'Predicted_Status', predictions) 
            
            # --- NEW REORDERING LOGIC ---
            # 2. Check if 'Student id' exists, and pull it to the front
            if 'Student id' in results_df.columns:
                cols = results_df.columns.tolist()
                cols.remove('Student id')        # Remove it from the back
                cols.insert(1, 'Student id')     # Insert it at index 1 (right after the prediction)
                results_df = results_df[cols]    # Apply the new order
            # -----------------------------

            return results_df, "Success"
            
        except Exception as e:
            return None, f"Prediction error: {str(e)}"