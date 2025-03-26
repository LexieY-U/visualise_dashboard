import streamlit as st
import pandas as pd
import boto3

# Use S3 bucket
s3 = boto3.client("s3")
bucket_name = "supply-chain-dummy-data"
file_name = "SupplyChain_Exceptions_Dummy_Data.xlsx"

# Test S3 access in Sagemaker
response = s3.list_objects_v2(Bucket=bucket_name)
print(response)

# ---- Load Data from Excel ----
# local version 
# file_path = r"C:\Users\jiyin.yu\OneDrive - Accenture\Desktop\SOD\visualise_dashboard\SupplyChain_Exceptions_Dummy_Data.xlsx"
# Remote version 
# file_path = "/home/ec2-user/environment/.c9/visualise_dashboard/SupplyChain_Exceptions_Dummy_Data.xlsx"

def load_data():
    try:
        # Fetch file from S3
        s3.get_object(Bucket=bucket_name, Key=file_name)
        df = pd.read_excel(f"s3://{bucket_name}/{file_name}", dtype=str)
        df.columns = df.columns.str.strip()  # Clean column names
        
        if "df" not in st.session_state:
            st.session_state.df = df
            st.session_state.edited_df = df.copy()
        return df
    
    except Exception as e:
        st.error(f"Error loading data from s3: {e}")
        return None
