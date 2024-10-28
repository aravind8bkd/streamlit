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

# Define a function for plotting FBS and PPBS readings
def plot_health_tracker(df):
    # Ensure 'DATE' is in datetime format
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%m-%Y')

    # Create the figure for FBS and PPBS
    fig = go.Figure()

    # Add FBS line
    fig.add_trace(go.Scatter(
        x=df['DATE'], 
        y=df['FBS'], 
        mode='lines+markers', 
        name='FBS', 
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    # Add PPBS line
    fig.add_trace(go.Scatter(
        x=df['DATE'], 
        y=df['PPBS'], 
        mode='lines+markers', 
        name='PPBS', 
        line=dict(color='red'),
        marker=dict(size=6)
    ))

    # Update layout for better appearance
    fig.update_layout(
        title='Blood Glucose Level',  # Updated plot title
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

# Define a function for plotting weight
def plot_weight(df):
    if 'Wt' in df.columns and df['Wt'].notna().any():  # Check if 'Wt' exists and has values
        # Create a bar plot for Weight
        weight_fig = go.Figure()
        weight_fig.add_trace(go.Bar(
            x=df['DATE'],
            y=df['Wt'],
            name='Weight',
            marker=dict(color='orange')
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

    df = get_data(csv_url)
    if df is not None:
        # Directly plot without checking for column names
        plot_health_tracker(df)
        plot_weight(df)  # Plot weight if available
    else:
        st.error("Failed to load data.")

if __name__ == "__main__":
    main()
