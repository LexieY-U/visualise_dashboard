import streamlit as st
import pandas as pd
import boto3
from io import BytesIO
import json

# Config AWS
s3 = boto3.client("s3")
bucket_name = "supply-chain-dummy-data"
xlsx_file_name = "SupplyChain_Exceptions_Dummy_Data.xlsx"
csv_file_name = "SupplyChain_Exceptions_Dummy_Data.csv"  # Converted file
bedrock = boto3.client(service_name="bedrock-runtime", region_name="eu-west-2")

# ---- Load Data from Excel ----
# local version 
# file_path = r"C:\Users\jiyin.yu\OneDrive - Accenture\Desktop\SOD\visualise_dashboard\SupplyChain_Exceptions_Dummy_Data.xlsx"
# Remote version 
# file_path = "/home/ec2-user/environment/.c9/visualise_dashboard/SupplyChain_Exceptions_Dummy_Data.xlsx"

# Converts Excel file to CSV and uploads it back to S3
def convert_excel_to_csv():
    try:
        # Fetch Excel file from S3
        response = s3.get_object(Bucket=bucket_name, Key=xlsx_file_name)
        df = pd.read_excel(BytesIO(response["Body"].read()), dtype=str)

        # Convert to CSV in memory
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding="utf-8")
        csv_buffer.seek(0)

        # Upload CSV to S3
        s3.put_object(Bucket=bucket_name, Key=csv_file_name, Body=csv_buffer.getvalue())

        st.success(f"Converted {xlsx_file_name} to {csv_file_name} and uploaded to S3.")
    
    except Exception as e:
        st.error(f"Error converting Excel to CSV: {e}")

def load_data():
    try:
        # Loads supply chain exception data from S3
        # Check if CSV exists in S3, otherwise convert from Excel
        existing_files = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
        file_names = [obj["Key"] for obj in existing_files]

        if csv_file_name not in file_names:
            st.warning(f"{csv_file_name} not found. Converting from Excel...")
            convert_excel_to_csv()

        # Fetch CSV file from S3
        response = s3.get_object(Bucket=bucket_name, Key=csv_file_name)
        df = pd.read_csv(BytesIO(response["Body"].read()), dtype=str)
       
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Store data in Streamlit session state
        if "df" not in st.session_state:
            st.session_state.df = df
            st.session_state.edited_df = df.copy()
        return df
    
    except Exception as e:
        st.error(f"Error loading data from s3: {e}")
        return None

# Generates a summary of supply chain exceptions using Claude 3 Sonnet in Bedrock
def generate_exception_report(df):  
    # Convert data to a text prompt
    summary_prompt = f"""
    Please analyse the supply chain csv file uploaded in S3 bucket. 
    Tell me how many open exceptions are there in the csv file.
    Below is a snapshot of recent exceptions:
    
    {df.head().to_string()}
    
    Based on this data, summarize the key critical in-flight problems.
    Highlight top recurring issues and urgent supply chain disruptions.
    Focus on the key insights, actionable recommendations, and any data points relevant for decision-making.
    """

    # Define the Bedrock request payload
    payload = {
        "prompt": summary_prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.7
    }

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    # Extract AI-generated report
    result = json.loads(response["body"].read())
    return result["completion"]
