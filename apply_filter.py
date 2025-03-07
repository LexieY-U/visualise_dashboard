# Define a func to apply filters
def apply_filters(df, selected_demand_units, selected_theatre, selected_priority, selected_last_checkpoint, selected_late_status):
    if selected_demand_units:
        df = df[df["Demanding_Unit"].isin(selected_demand_units)]
    if selected_theatre:
        df = df[df["Theatre"].isin(selected_theatre)]
    if selected_priority:
        df = df[df["Priority"].isin(selected_priority)]
    if selected_last_checkpoint:
        df = df[df["Last_JSC_Checkpoint"].isin(selected_last_checkpoint)]
    if selected_late_status:
        df = df[df["Late_Status"].isin(selected_late_status)]
    return df