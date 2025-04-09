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
bedrock = boto3.client(service_name="bedrock-runtime")

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
        s3_path = f"s3://{bucket_name}/{csv_file_name}"
        response = s3.get_object(Bucket=bucket_name, Key=csv_file_name)
        df = pd.read_csv(BytesIO(response["Body"].read()), dtype=str)
       
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Store data in Streamlit session state
        if "df" not in st.session_state:
            st.session_state.df = df
            st.session_state.edited_df = df.copy()
        return df, s3_path
    
    except Exception as e:
        st.error(f"Error loading data from s3: {e}")
        return None, None

# Generates a summary of supply chain exceptions using Claude 3 Sonnet in Bedrock
def generate_exception_report(df):
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    messages = [
        {"role": "user",
         "content": f"""
            Below is a snapshot of recent supply chain exceptions:
            
            {df.head().to_string()}

            Please analyse this data and provide a structured report in the following Markdown format:

            ## Supply Chain Exception Report

            **1. How many open exceptions are there?**  
            <Provide the answer here>

            **2. What are the key critical in-flight problems?**  
            <Provide the answer here>

            **3. What are the top recurring issues?**  
            <Provide the answer here>

            **4. What urgent supply chain disruptions exist?**  
            <Provide the answer here>

            **5. Actionable insights and recommendations:**  
            - **a.** <Recommendation 1>  
            - **b.** <Recommendation 2>  
            - **c.** <Recommendation 3>  
            - **d.** <Recommendation 4>  
            - **e.** <Recommendation 5>  
            - **f.** <Recommendation 6>  
            - **g.** <Recommendation 7>  

            Ensure that the response strictly follows this format and replaces the placeholders with actual insights from the data.
        """}
    ]
    
    payload = {
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.5,
        "anthropic_version": "bedrock-2023-05-31"
    }

    request = json.dumps(payload)

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=request,
            contentType="application/json",
            accept="application/json"
        )
        
    except Exception as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return None

    model_response = json.loads(response["body"].read())

    # Extract the response correctly
    return model_response["content"]


def generate_report_and_display():
    df = st.session_state.get("df", None)
    if df is not None:
        with st.spinner("Generating AI-powered exception report..."):
            report = generate_exception_report(df)
            if report:
                st.success("Report generated successfully!")

                # Extract the text content
                report_text = report[0]["text"] if isinstance(report, list) and "text" in report[0] else "No valid response received."

                # Format report with Markdown for better readability
                formatted_report = f"""
                ### AI-Powered Supply Chain Exception Report

                {report_text.replace("1.", "**1.**").replace("2.", "**2.**")
                .replace("3.", "**3.**").replace("4.", "**4.**")
                .replace("5.", "**5.**")}

                """

                # Display nicely formatted report
                st.markdown(formatted_report)

                # Prepare report content for download
                report_bytes = formatted_report.encode("utf-8")  # Convert string to bytes
                report_buffer = BytesIO(report_bytes)  # Create BytesIO buffer
                report_buffer.seek(0)  # Reset buffer position

                # Provide a download button
                st.download_button(
                    label="Download Report",
                    data=report_buffer,
                    file_name="SupplyChain_Exception_Report.txt",
                    mime="text/plain",
                )

            else:
                st.error("Failed to generate a valid report. Please try again.")

    else:
        st.error("No data found! Please load the supply chain data first.")
