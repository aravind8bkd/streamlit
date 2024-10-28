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
def plot_health_tracker(df, freq):
    # Ensure 'DATE' is in datetime format
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%m-%Y')
    
    # Group data by specified frequency
    df_grouped = df.groupby(pd.Grouper(key='DATE', freq=freq)).mean().reset_index()

    # Create the figure
    fig = go.Figure()

    # Add FBS line
    fig.add_trace(go.Scatter(
        x=df_grouped['DATE'], 
        y=df_grouped['FBS'], 
        mode='lines+markers', 
        name='FBS', 
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    # Add PPBS line
    fig.add_trace(go.Scatter(
        x=df_grouped['DATE'], 
        y=df_grouped['PPBS'], 
        mode='lines+markers', 
        name='PPBS', 
        line=dict(color='red'),
        marker=dict(size=6)
    ))

    # Add the normal range for FBS and PPBS
    fig.add_trace(go.Scatter(
        x=df_grouped['DATE'],
        y=[100]*len(df_grouped['DATE']),
        mode='lines',
        name='FBS Normal Range',
        line=dict(color='green', width=0.5, dash='dash'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=df_grouped['DATE'],
        y=[140]*len(df_grouped['DATE']),
        mode='lines',
        name='PPBS Normal Range',
        line=dict(color='green', width=0.5, dash='dash'),
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

    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Streamlit App Layout
def main():
    st.title("Health Tracker")  # Main title for Streamlit

    # Dropdown to select date frequency
    freq = st.selectbox(
        'Select the frequency for date grouping:',
        options=['D', 'M', 'Q', 'Y'],
        format_func=lambda x: {'D': 'Daily', 'M': 'Monthly', 'Q': 'Quarterly', 'Y': 'Yearly'}[x]
    )

    df = get_data(csv_url)
    if df is not None:
        # Check for exact column names: 'DATE', 'FBS', and 'PPBS'
        if 'DATE' in df.columns and 'FBS' in df.columns and 'PPBS' in df.columns:
            plot_health_tracker(df, freq)
        else:
            st.error("The CSV must contain 'DATE', 'FBS', and 'PPBS' columns.")
    else:
        st.error("Failed to load data.")

if __name__ == "__main__":
    main()
