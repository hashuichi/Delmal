import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.title('Dashboard')
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

    # Sidebar to select filter options
    st.sidebar.header('Filter Options')

    # Date filtering options
    filter_by = st.sidebar.selectbox('Filter by', ['Day', 'Month', 'Year'])

    if filter_by == 'Day':
        selected_date = st.sidebar.date_input('Select a date', min_value=df['Date'].min(), max_value=df['Date'].max())
        filtered_df = df[df['Date'] == selected_date.strftime("%Y-%m-%d")]
    elif filter_by == 'Month':
        selected_month = st.sidebar.slider('Select a month', 1, 12, 1)
        selected_year = st.sidebar.slider('Select a year', df['Date'].dt.year.min(), df['Date'].dt.year.max())
        filtered_df = df[(df['Date'].dt.month == selected_month) & (df['Date'].dt.year == selected_year)]
    else:  
        selected_year = st.sidebar.slider('Select a year', df['Date'].dt.year.min(), df['Date'].dt.year.max())
        filtered_df = df[df['Date'].dt.year == selected_year]

    # Display the filtered DataFrame
    st.subheader('Filtered DataFrame')
    st.write(filtered_df)

if __name__ == "__main__":
    main()