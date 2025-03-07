import streamlit as st
import pandas as pd
from apply_filter import apply_filters
from config import exception_status_options, intervention_action_taken_options, exception_outcome_options
from data_loader import load_data
from data_utils import save_edits
from visualisations import plot_stacked_bar_chart, plot_bar_chart, plot_exceptions_overview

# Load data
df = load_data()

# Streamlit Layout
st.title("Supply Chain Exceptions Dashboard")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Exception Detection", "Exceptions Management", "Historic Exceptions"])

# Create a sidebar and add dropdown filters
st.sidebar.title("Customer Filters")
selected_demand_units = st.sidebar.multiselect("Demanding Unit", options=sorted(df["Demanding_Unit"].unique()))
selected_theatre = st.sidebar.multiselect("Theatre", options=sorted(df["Theatre"].unique()))
selected_priority = st.sidebar.multiselect("Priority", options=sorted(df["Priority"].unique()))
selected_last_checkpoint = st.sidebar.multiselect("Last JSC Checkpoint", options=sorted(df["Last_JSC_Checkpoint"].unique()))
selected_late_status = st.sidebar.multiselect("Late Status", options=sorted(df["Late_Status"].unique()))

with tab1:
    st.markdown("**Projected Disruptions**")
    filtered_df = apply_filters(df, selected_demand_units, selected_theatre, selected_priority, selected_last_checkpoint, selected_late_status)
    
    st.plotly_chart(plot_stacked_bar_chart(filtered_df), key="stacked_chart_tab1")
    st.plotly_chart(plot_bar_chart(filtered_df), key="bar_chart_tab1")

    # Editable Data Table (Only show rows where "Raised_As_Exception?" is empty)
    editable_df = st.session_state.edited_df[st.session_state.edited_df["Raised_As_Exception?"].fillna("") == ""]
    edited_df = st.data_editor(editable_df, column_config={
        "Exception_Status": st.column_config.SelectboxColumn("Exception_Status", options=exception_status_options, required=True),
        "Intervention_Action_Taken": st.column_config.SelectboxColumn("Intervention_Action_Taken", options=intervention_action_taken_options, required=True),
        "Exception_Outcome": st.column_config.SelectboxColumn("Exception_Outcome", options=exception_outcome_options, required=True),
    }, hide_index=True, key="data_editor_tab1")

    st.session_state.edited_df.loc[edited_df.index] = edited_df

    if st.button("Save Changes", key="save_tab1"):
        save_edits()

with tab2:
    st.header("Exceptions Management")
    st.markdown(" :gray[Live Orders Raised as an Exception]")

    # Filter dataframe to only show rows where 'Raised_As_Exception?' == 'Yes'
    df_tab2 = df[df['Raised_As_Exception?'] == 'Yes']
    filtered_df = apply_filters(df_tab2, selected_demand_units, selected_theatre, selected_priority, selected_last_checkpoint, selected_late_status)

    # Plot Exceptions Overview
    st.plotly_chart(plot_exceptions_overview(filtered_df), key="exceptions_overview_chart")

    # Editable Data Table (Only show rows where "Raised_As_Exception?" is "Yes")
    editable_df = st.session_state.edited_df[st.session_state.edited_df["Raised_As_Exception?"] == "Yes"]
    edited_df = st.data_editor(editable_df, column_config={
        "Exception_Status": st.column_config.SelectboxColumn("Exception_Status", options=exception_status_options, required=True),
        "Intervention_Action_Taken": st.column_config.SelectboxColumn("Intervention_Action_Taken", options=intervention_action_taken_options, required=True),
        "Exception_Outcome": st.column_config.SelectboxColumn("Exception_Outcome", options=exception_outcome_options, required=True),
    }, hide_index=True, key="data_editor_tab2")

    st.session_state.edited_df.loc[edited_df.index] = edited_df

    if st.button("Save Changes", key="save_tab2"):
        save_edits()


with tab3:
    st.header("Historic Exceptions")
    st.markdown(" :gray[Historic Exceptions Managed to Resolution]")

    # Filter dataframe to only show rows where 'Raised_As_Exception?' == 'Yes' AND 'Exception_Status' is 'Closed'
    historic_df = df[(df["Raised_As_Exception?"] == "Yes") & (df["Exception_Status"] == "5. Exception Closed")]
    filtered_df = apply_filters(historic_df, selected_demand_units, selected_theatre, selected_priority, selected_last_checkpoint, selected_late_status)

    # Plot Historic Exceptions Overview
    st.plotly_chart(plot_exceptions_overview(filtered_df), key="historic_exceptions_chart")

    # Display the Historic Exceptions DataFrame
    st.write(filtered_df)  # Shows all historic exceptions that have been resolved
