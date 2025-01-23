import streamlit as st
import pandas as pd


# ---- Load Data from Excel ----
# local version 
file_path = r"C:\Users\jiyin.yu\OneDrive - Accenture\Desktop\SOD\visualise_dashboard\SupplyChain_Exceptions_Dummy_Data.xlsx"
# Remote version 
# file_path = "/home/ec2-user/environment/.c9/visualise_dashboard/SupplyChain_Exceptions_Dummy_Data.xlsx"

# Read Excel file into pandas DataFrame
df = pd.read_excel(file_path)


# Streamlit Layout
st.title("Supply Chain Exceptions Dashboard")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Exception Detection", "Exception Management", "Historic Exceptions"])

with tab1:
    st.header("Exception Detection")  # Bold the title for the first chart
    st.markdown("### **Projected Disruptions**")  # Bold and set as a larger heading
    st.markdown(" :gray[> 50% chance of missing delivery SLA]")  # Subtitle below the title