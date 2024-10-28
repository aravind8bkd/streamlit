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

    # Create the figure
    fig = go.Figure()

    # Add FBS line
    fig.add_trace(go.Scatter(
        x=df['DATE'], 
        y=df['FBS'], 
        mode='lines+markers', 
        name='FBS', 
        line=dict(color='blue'),
        marker=dict(size=6),
        hovertemplate='Date: %{x|%b-%Y}<br>FBS: %{y}<extra></extra>'  # Custom hover info
    ))

    # Add PPBS line
    fig.add_trace(go.Scatter(
        x=df['DATE'], 
        y=df['PPBS'], 
        mode='lines+markers', 
        name='PPBS', 
        line=dict(color='red'),
        marker=dict(size=6),
        hovertemplate='Date: %{x|%b-%Y}<br>PPBS: %{y}<extra></extra>'  # Custom hover info
    ))

    # Define normal range values
    fbs_normal_upper = 100
    ppbs_normal_upper = 140

    # Add area fill between the normal range
    fig.add_trace(go.Scatter(
        x=pd.concat([df['DATE'], df['DATE'][::-1]]),  # Dates for area fill
        y=pd.concat([[0] * len(df), [fbs_normal_upper]*len(df)[::-1]]),  # Fill from 0 to 100 for FBS
        fill='toself',  # Fill area
        fillcolor='rgba(144, 238, 144, 0.5)',  # Light green color with transparency
        name='Normal Range for FBS',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=pd.concat([df['DATE'], df['DATE'][::-1]]),  # Dates for area fill
        y=pd.concat([[fbs_normal_upper] * len(df), [ppbs_normal_upper]*len(df)[::-1]]),  # Fill from 100 to 140 for PPBS
        fill='toself',  # Fill area
        fillcolor='rgba(144, 238, 144, 0.5)',  # Light green color with transparency
        name='Normal Range for PPBS',
        showlegend=False
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

# Streamlit App Layout
def main():
    st.title("Health Tracker")  # Main title for Streamlit

    df = get_data(csv_url)
    if df is not None:
        # Check for exact column names: 'DATE', 'FBS', and 'PPBS'
        if 'DATE' in df.columns and 'FBS' in df.columns and 'PPBS' in df.columns:
            plot_health_tracker(df)
        else:
            st.error("The CSV must contain 'DATE', 'FBS', and 'PPBS' columns.")
    else:
        st.error("Failed to load data.")

if __name__ == "__main__":
    main()

