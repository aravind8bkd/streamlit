import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# URL of the raw CSV file from GitHub - replace with your actual URL
csv_url = "https://raw.githubusercontent.com/aravind8bkd/streamlit/refs/heads/main/myhealthtracker.csv"

# Function to fetch data from the provided CSV URL
def get_data(csv_url):
    try:
        # Read the CSV
        df = pd.read_csv(csv_url, 
                         delimiter=',',  # Assuming the CSV is comma-separated
                         encoding='utf-8', 
                         skip_blank_lines=True
                         )
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

# Function to aggregate data based on the selected frequency
def aggregate_data(df, frequency):
    # Ensure 'DATE' is in datetime format
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%m-%Y')
    
    # Set 'DATE' as the index for resampling
    df.set_index('DATE', inplace=True)
    
    # Aggregate data based on frequency
    if frequency == 'Monthly':
        aggregated_df = df.resample('M').mean()  # Taking the mean for monthly aggregation
    elif frequency == 'Quarterly':
        aggregated_df = df.resample('Q').mean()  # Taking the mean for quarterly aggregation
    elif frequency == 'Yearly':
        aggregated_df = df.resample('Y').mean()  # Taking the mean for yearly aggregation
    elif frequency == 'All Data Points':
        aggregated_df = df  # No aggregation, use all data points
    else:
        aggregated_df = df

    # Reset index for plotting
    aggregated_df.reset_index(inplace=True)
    return aggregated_df

# Define a function for plotting FBS and PPBS readings
def plot_health_tracker(df):
    # Create the figure for FBS and PPBS
    fig = go.Figure()

    # Add FBS line (connect non-consecutive points)
    fig.add_trace(go.Scatter(
        x=df['DATE'], 
        y=df['FBS'],
        mode='lines+markers', 
        name='FBS', 
        line=dict(color='blue'),
        marker=dict(size=6),
        connectgaps=True  # Connect non-consecutive points
    ))

    # Add PPBS line (connect non-consecutive points)
    fig.add_trace(go.Scatter(
        x=df['DATE'], 
        y=df['PPBS'], 
        mode='lines+markers', 
        name='PPBS', 
        line=dict(color='red'),
        marker=dict(size=6),
        connectgaps=True  # Connect non-consecutive points
    ))

    # Update layout for better appearance
    fig.update_layout(
        title='Blood Glucose Level',
        xaxis_title='Date',
        yaxis_title='Blood Sugar Readings (mg/dL)',
        yaxis=dict(range=[0, 200]),  # Set the range of Y-axis
        hovermode='x unified'
    )

    # Update x-axis to automatically adjust tick spacing based on zoom
    fig.update_xaxes(
        tickformat="%b-%Y",  # Format for x-axis labels
        tickangle=-45,  # Angle for better visibility
        showspikes=True,  # Optional: Show spikes on hover
        spikemode="across",  # Optional: Cross-mode for spikes
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Define a function for plotting weight as a line plot
def plot_weight(df):
    if 'Wt' in df.columns and df['Wt'].notna().any():  # Check if 'Wt' exists and has values
        # Create a line plot for Weight
        weight_fig = go.Figure()
        weight_fig.add_trace(go.Scatter(
            x=df['DATE'],
            y=df['Wt'],
            mode='lines+markers',  # Line with markers
            name='Weight',
            line=dict(color='orange', width=2),
            marker=dict(size=6),
            connectgaps=True  # Connect non-consecutive points
        ))

        # Add target weight line at 80kg in bold green color
        weight_fig.add_trace(go.Scatter(
            x=df['DATE'],
            y=[80]*len(df['DATE']),  # Constant line at y=80
            mode='lines',  # Only line
            name='Target Weight (80kg)',
            line=dict(color='green', width=4, dash='solid'),  # Bold green line
            showlegend=True
        ))

        # Update layout for better appearance
        weight_fig.update_layout(
            title='Weight Over Time',
            xaxis_title='Date',
            yaxis_title='Weight (kg)',
            yaxis=dict(range=[0, df['Wt'].max() + 10]),  # Set Y-axis range based on weight data
            hovermode='x unified'
        )

        # Update x-axis for weight plot
        weight_fig.update_xaxes(
            tickformat="%b-%Y",
            tickangle=-45,
            showspikes=True,
            spikemode="across",
        )

        # Display the weight plot in Streamlit
        st.plotly_chart(weight_fig)
    else:
        st.warning("Weight data is not available or has no valid entries.")

# Streamlit App Layout
def main():
    st.title("Health Tracker")  # Main title for Streamlit
    st. set_page_config(layout="wide") 
    df = get_data(csv_url)
    if df is not None:
        # Dropdown for date aggregation with default set to 'Yearly'
        frequency = st.selectbox(
            "Select Date Aggregation:",
            ["Monthly", "Quarterly", "Yearly", "All Data Points"],
            index=2  # Set default index to 'Yearly' (third option)
        )
        
        # Aggregate data based on the selected frequency
        aggregated_df = aggregate_data(df, frequency)

        # Plot health tracker and weight plots with aggregated data
        plot_health_tracker(aggregated_df)
        plot_weight(aggregated_df)  # Plot weight if available
    else:
        st.error("Failed to load data.")

if __name__ == "__main__":
    main()
