import pandas as pd
import streamlit as st
from data_loader import file_path

def save_edits():
    updated_df = st.session_state.edited_df.copy()

    # Identify rows where "Exception_Status" was previously empty and now has a value
    mask = (st.session_state.df["Exception_Status"].fillna("") == "") & (updated_df["Exception_Status"].fillna("") != "")

    # Update "Raised_As_Exception?" to "Yes" only for those rows
    updated_df.loc[mask, "Raised_As_Exception?"] = "Yes"

    # Write back to the Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        updated_df.to_excel(writer, index=False)

    # Update session state to reflect changes
    st.session_state.df = updated_df
    st.session_state.edited_df = updated_df

    st.success("Changes saved successfully!")
