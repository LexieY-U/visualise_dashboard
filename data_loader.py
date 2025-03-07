import streamlit as st
import pandas as pd

# ---- Load Data from Excel ----
# local version 
file_path = r"C:\Users\jiyin.yu\OneDrive - Accenture\Desktop\SOD\visualise_dashboard\SupplyChain_Exceptions_Dummy_Data.xlsx"
# Remote version 
# file_path = "/home/ec2-user/environment/.c9/visualise_dashboard/SupplyChain_Exceptions_Dummy_Data.xlsx"
# Read Excel file into pandas DataFrame
# print(df.dtypes)
def load_data():
    df = pd.read_excel(file_path, dtype=str)
    df.columns = df.columns.str.strip()  # Clean column names

    if "df" not in st.session_state:
        st.session_state.df = df
        st.session_state.edited_df = df.copy()

    return df