import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

def load_course_data(file_path: str):
    """Loads CSV and converts rows to LangChain Documents."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return None
    
    df['page_content'] = df.apply(
        lambda row: f"Course Title: {row['course_title']}\n"
                    f"Subject: {row['subject']}\n"
                    f"Level: {row['level']}\n"
                    f"Duration: {row['content_duration']}\n"
                    f"Price: ${row['price']}\n"
                    f"Paid: {'Yes' if row['is_paid'] else 'No'}",
        axis=1
    )
    
    loader = DataFrameLoader(df, page_content_column="page_content")
    return loader.load()