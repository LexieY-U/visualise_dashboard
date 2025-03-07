import plotly.graph_objects as go

def plot_stacked_bar_chart(df):
    # Aggregate data for each priority
    total_orders = df.groupby('Priority').size()
    projected_late = df[df['Late_Status'] == "Projected Late"].groupby('Priority').size()
    already_late = df[df['Late_Status'] == "Already Late"].groupby('Priority').size()

    # Handle missing categories (in case there are no orders in a category)
    projected_late = projected_late.reindex(total_orders.index, fill_value=0)
    already_late = already_late.reindex(total_orders.index, fill_value=0)
    

    # Create the horizontal bar chart
    fig = go.Figure()

    # Stacked bar chart for each category
    fig.add_trace(go.Bar(
        y=total_orders.index,
        x=total_orders,
        name="Total Orders",
        orientation='h',
        marker_color="#6A0DAD",  # Purple
        text=total_orders,
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        y=projected_late.index,
        x=projected_late,
        name="Projected Late Orders",
        orientation='h',
        marker_color="#FFA500",  # Orange
        text=projected_late,
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        y=already_late.index,
        x=already_late,
        name="Already Late Orders",
        orientation='h',
        marker_color="#FF0000",  # Red
        text=already_late,
        textposition='inside'
    ))


    fig.update_layout(
        barmode='stack',  # Stack bars for each priority
        title="Projected Disruptions by Priority",
        xaxis_title="Number of Orders",
        yaxis_title="Priority",
        legend_title="Metrics",
        template="plotly_white",
    )
    
    return fig

def plot_bar_chart(df):
    stages = df["Last_JSC_Checkpoint"].unique()
    categories = ["Projected On Time", "Projected Late", "Already Late"]
    colors = {"Projected On Time": "green", "Projected Late": "orange", "Already Late": "red"}

    fig = go.Figure()
    for category in categories:
        filtered_df = df[df["Late_Status"] == category]
        values = [filtered_df[filtered_df["Last_JSC_Checkpoint"] == stage].shape[0] for stage in stages]
        fig.add_trace(go.Bar(
            y=stages, x=values, name=category, orientation='h', 
            marker=dict(color=colors[category]), showlegend=True))

    fig.update_layout(
        barmode='stack',
        title="Projected Disruptions by Stage",
        xaxis_title="Count",
        yaxis_title="Stage",
        template="plotly_white",
        xaxis=dict(tickformat=",", showgrid=True, zeroline=False),  # Add commas to number format
        yaxis=dict(tickangle=0),  # Rotate y-axis labels for better visibility
        margin=dict(l=50, r=50, t=50, b=50)  # Add margins to prevent overcrowding
    )
    return fig

def plot_exceptions_overview(df):
    priority_counts = df['Priority'].value_counts().reindex(['P1', 'P2', 'P3'], fill_value=0)

    # Create a horizontal bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=priority_counts.index,
        x=priority_counts.values,
        orientation='h',
        marker_color=["#6A0DAD", "#FFA500", "#FF0000"],  # Custom colors for P1, P2, P3
        text=priority_counts.values,
        textposition="inside"
    ))

    fig.update_layout(
        title="Exceptions Management Overview",
        xaxis_title="Number of Orders",
        yaxis_title="Priority",
        template="plotly_white",
        showlegend=False
    )

    return fig