import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV link (with dl=1 for direct download)
url = "https://github.com/aravind8bkd/streamlit/blob/main/myhealthtracker.csv"

# Function to fetch data from Dropbox CSV
def get_dropbox_data(csv_url):
    try:
        # Read the CSV with correct settings
        df = pd.read_csv(csv_url, 
                         delimiter=',',        # Adjust delimiter if needed
                         encoding='utf-8',     # Explicitly specify encoding
                         quotechar='"',        # Handling special characters in quotes
                         skip_blank_lines=True # Skip blank lines if they exist
                         )
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

# Define a function for plotting FBS and PPBS readings
def plot_health_tracker(df):
    st.title("Health Tracker")  # Updated title for Streamlit

    # Ensure 'DATE' is in datetime format
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot FBS and PPBS readings
    ax.plot(df['DATE'], df['FBS'], label='FBS', marker='o', color='blue')
    ax.plot(df['DATE'], df['PPBS'], label='PPBS', marker='o', color='red')

    # Plot the normal range (green area)
    ax.fill_between(df['DATE'], 70, 100, color='green', alpha=0.1, label="Normal FBS Range")
    ax.fill_between(df['DATE'], 100, 140, color='green', alpha=0.1, label="Normal PPBS Range")

    # Adding labels and updated title for the plot
    ax.set_title('Health Tracker')  # Updated title for the plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Blood Sugar Readings (mg/dL)')
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)

# Streamlit App Layout
def main():
    st.header("Health Tracker")  # Updated header for Streamlit

    df = get_dropbox_data(url)
    if df is not None:
        # Check for exact column names: 'DATE', 'FBS', and 'PPBS'
        if 'DATE' in df.columns and 'FBS' in df.columns and 'PPBS' in df.columns:
            plot_health_tracker(df)
        else:
            st.error("The sheet must contain 'DATE', 'FBS', and 'PPBS' columns.")
    else:
        st.error("Failed to load data.")

if __name__ == "__main__":
    main()
