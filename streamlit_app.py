import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Hardcoded public Google Sheet URL
public_sheet_url = "https://drive.google.com/file/d/1isYg80aXAVcifyV0QH5Eyuzl9MCYlu6Q/view?usp=sharing"

# Function to fetch data from a public Google Sheet
def get_gsheet_data(sheet_url):
    # Convert the Google Sheet URL into a CSV export URL
    csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    
    # Read the data into a DataFrame
    df = pd.read_csv(csv_export_url)
    
    return df

# Define a function for plotting FBS and PPBS readings
def plot_health_tracker(df):
    st.title("My Health Tracker")

    # Ensure 'Date' is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot FBS and PPBS readings
    ax.plot(df['Date'], df['FBS'], label='FBS', marker='o', color='blue')
    ax.plot(df['Date'], df['PPBS'], label='PPBS', marker='o', color='red')

    # Plot the normal range (green area)
    # Normal FBS range: 70-100 mg/dL, Normal PPBS range: 100-140 mg/dL
    ax.fill_between(df['Date'], 70, 100, color='green', alpha=0.1, label="Normal FBS Range")
    ax.fill_between(df['Date'], 100, 140, color='green', alpha=0.1, label="Normal PPBS Range")

    # Adding labels and title
    ax.set_title('My Health Tracker')
    ax.set_xlabel('Date')
    ax.set_ylabel('Blood Sugar Readings (mg/dL)')
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)

# Streamlit App Layout
def main():
    st.header("Google Sheets Data Dashboard")

    try:
        # Fetch and display the data
        df = get_gsheet_data(public_sheet_url)
        if 'Date' in df.columns and 'FBS' in df.columns and 'PPBS' in df.columns:
            plot_health_tracker(df)
        else:
            st.error("The sheet must contain 'Date', 'FBS', and 'PPBS' columns.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
