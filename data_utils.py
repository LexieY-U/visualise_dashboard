import streamlit as st
import boto3
import io

# AWS S3 Config
s3 = boto3.client("s3")
bucket_name = "supply-chain-dummy-data"
csv_file_name = "SupplyChain_Exceptions_Dummy_Data.csv"

def save_edits(s3_path):
    try:
        updated_df = st.session_state.edited_df.copy()
    
        # Identify rows where "Exception_Status" was previously empty and now has a value
        mask = (st.session_state.df["Exception_Status"].fillna("") == "") & (updated_df["Exception_Status"].fillna("") != "")
    
        # Update "Raised_As_Exception?" to "Yes" only for those rows
        updated_df.loc[mask, "Raised_As_Exception?"] = "Yes"
    
        # Convert DataFrame to CSV and upload to S3
        csv_buffer = io.StringIO()
        updated_df.to_csv(csv_buffer, index=False, encoding="utf-8")
        s3.put_object(Bucket=bucket_name, Key=csv_file_name, Body=csv_buffer.getvalue())
    
        # Update session state to reflect changes
        st.session_state.df = updated_df
        st.session_state.edited_df = updated_df
    
        st.success("Changes saved successfully!")

    except Exception as e:
        st.error(f"Error saving changes to S3: {e}")
