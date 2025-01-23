import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
    st.markdown("**Projected Disruptions**")  # Bold and set as a larger heading
    st.markdown(" :gray[> 50% chance of missing delivery SLA]")  # Subtitle below the title


    priority_data = {
    "Priority": ["P1 Orders", "P2 Orders", "P3 Orders"],
    "Total Orders": [50, 61, 45],
    "Projected Late Orders": [25, 28, 21],
    "Already Late Orders": [11, 16, 8],
    "Open Exceptions": [2, 1, 0],
}

    # Convert to DataFrame
    priority_df = pd.DataFrame(priority_data)

    # Plotly Horizontal Bar Chart
    fig = go.Figure()

    # Add bars for each metric with respective numbers
    fig.add_trace(go.Bar(
        y=priority_df["Priority"], 
        x=priority_df["Total Orders"], 
        name="Total Orders", 
        orientation='h',
        marker_color="#6A0DAD",  # Purple
        text=priority_df["Total Orders"],  # Display numbers
        textposition='auto'  # Auto positions the text
    ))
    fig.add_trace(go.Bar(
        y=priority_df["Priority"], 
        x=priority_df["Projected Late Orders"], 
        name="Projected Late Orders", 
        orientation='h',
        marker_color="#FFA500",  # Orange
        text=priority_df["Projected Late Orders"],  # Display numbers
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        y=priority_df["Priority"], 
        x=priority_df["Already Late Orders"], 
        name="Already Late Orders", 
        orientation='h',
        marker_color="#FF0000",  # Red
        text=priority_df["Already Late Orders"],  # Display numbers
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        y=priority_df["Priority"], 
        x=priority_df["Open Exceptions"], 
        name="Open Exceptions", 
        orientation='h',
        marker_color="#B22222",  # Dark Red
        text=priority_df["Open Exceptions"],  # Display numbers
        textposition='auto'
    ))

    # Update layout
    fig.update_layout(
        barmode='stack',  # Stacked bars for each priority
        title="Projected Disruptions",
        xaxis_title="Number of Orders",
        yaxis_title="Priority",
        legend_title="Metrics",
        template="plotly_white"
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # The second bar chart - Projected Disruptions by Stage
    st.markdown("**Projected Disruptions by Stages**")  # Bold and set as a larger heading

    # Sample data
    data_projected_disruptions_by_stage = {
        "Stages": [
            "Arrived PoD",
            "Pick & Packed",
            "Arrived PoE",
            "Demand Raised",
            "Departed Depot",
            "Departed PoE",
            "Departed PoD",
        ],
        "Already Late": [0, 0, 11, 4, 10, 5, 5],
        "Projected Late": [7, 9, 11, 19, 0, 0, 28],
        "Projected On Time": [4, 6, 8, 5, 2, 6, 16],
    }

    df = pd.DataFrame(data_projected_disruptions_by_stage)

    # Create a stacked bar chart with Plotly
    fig = go.Figure()

    # Add traces for each category
    fig.add_trace(go.Bar(
        y=df["Stages"],
        x=df["Already Late"],
        name="Already Late",
        orientation='h',
        marker=dict(color="red"),
        text=df["Already Late"],  # Add text to show numbers
        textposition="inside"    # Position the numbers inside the bars
    ))
    fig.add_trace(go.Bar(
        y=df["Stages"],
        x=df["Projected Late"],
        name="Projected Late",
        orientation='h',
        marker=dict(color="orange"),
        text=df["Projected Late"],
        textposition="inside"
    ))
    fig.add_trace(go.Bar(
        y=df["Stages"],
        x=df["Projected On Time"],
        name="Projected On Time",
        orientation='h',
        marker=dict(color="green"),
        text=df["Projected On Time"],
        textposition="inside"
    ))

    # Update layout
    fig.update_layout(
        barmode='stack',
        title=dict(
            text="Projected Disruptions by Stages",
            font=dict(size=16)  # Smaller title
        ),
        xaxis_title="Number of Orders",
        yaxis_title="Last JSC Checkpoint",
        legend_title="Metrics",
        template="plotly_white"
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)