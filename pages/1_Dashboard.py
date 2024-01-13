import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

with open("styles.css", "r") as f:
    css_content = f.read()

st.markdown(f"""
    <style>
        {css_content}
    </style>
""", unsafe_allow_html=True)

currency = 'SAR'

def calculate_metrics(df):
    total_revenue = (df['Price'] * df['Quantity']).sum()
    total_expenditure = (df['Cost'] * df['Quantity']).sum()
    gross_profit = total_revenue - total_expenditure
    gross_profit_margin = (gross_profit / total_revenue) * 100 if total_revenue != 0 else 0
    cash_reserves = total_revenue - total_expenditure
    burn_rate = total_expenditure / len(df['Date'].unique()) if len(df['Date'].unique()) != 0 else 0
    
    return (
        round(total_revenue),
        round(total_expenditure),
        round(gross_profit_margin),
        round(cash_reserves),
        round(burn_rate)
    )

def create_5_year_projection(df):
    # Create a DataFrame with a date range for the next 5 years
    end_date = df['Date'].max() + pd.DateOffset(years=5)
    date_range = pd.date_range(start=df['Date'].min(), end=end_date, freq='MS')  # MS: Month Start
    projection_df = pd.DataFrame(date_range, columns=['Date'])

    # Calculate monthly revenue and expenses for the projection
    projection_df['Revenue'] = 0
    projection_df['Expenses'] = 0

    for index, row in projection_df.iterrows():
        month_data = df[(df['Date'].dt.month == row['Date'].month) & (df['Date'].dt.year == row['Date'].year)]
        projection_df.loc[index, 'Revenue'] = (month_data['Price'] * month_data['Quantity']).sum()
        projection_df.loc[index, 'Expenses'] = (month_data['Cost'] * month_data['Quantity']).sum()

    return projection_df

def plot_histogram(df):
    # Plot the histogram of monthly revenue vs expenses
    plt.figure(figsize=(10, 6))
    plt.bar(df['Date'], df['Price'] * df['Quantity'], color='blue', alpha=0.7, label='Revenue')
    plt.bar(df['Date'], df['Cost'] * df['Quantity'], color='red', alpha=0.7, label='Expenses')
    
    plt.title('5-Year Projection: Monthly Revenue vs Expenses')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    
    st.pyplot()

def main():
    st.title('Dashboard')
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

    # Sidebar to select filter options
    st.sidebar.header('Filter Options')

    # Date filtering options
    filter_by = st.sidebar.selectbox('Filter by', ['Day', 'Month', 'Year'], label_visibility="collapsed")

    if filter_by == 'Day':
        selected_date = st.sidebar.date_input('Select a date', min_value=df['Date'].min(), max_value=datetime.now())
        filtered_df = df[df['Date'] == selected_date.strftime("%Y-%m-%d")]
    elif filter_by == 'Month':
        selected_month = st.sidebar.slider('Select a month', 1, 12, 1)
        selected_year = st.sidebar.slider('Select a year', df['Date'].dt.year.min(), df['Date'].dt.year.max())
        filtered_df = df[(df['Date'].dt.month == selected_month) & (df['Date'].dt.year == selected_year)]
    else:  
        selected_year = st.sidebar.slider('Select a year', df['Date'].dt.year.min(), df['Date'].dt.year.max())
        filtered_df = df[df['Date'].dt.year == selected_year]

    total_revenue, total_expenditure, gross_profit_margin, cash_reserves, burn_rate = calculate_metrics(filtered_df)
    page_col1, page_col2 = st.columns([1,1])

    with page_col1:
        with st.container():
            col1, col2, col3, col4, = st.columns(4)
            col1.write("<h1>💰</h1>", unsafe_allow_html=True)
            col2.write("<h2 class='metric_currency'>{}</h2>".format(currency), unsafe_allow_html=True)
            col3.write("<h2>{}</h2>".format(total_revenue), unsafe_allow_html=True)
            col4.write("<h3 class='metric_name'>Revenue</h3>", unsafe_allow_html=True)
            st.divider()
        with st.container():
            col1, col2, col3, col4, = st.columns(4)
            col1.write("<h1>💸</h1>", unsafe_allow_html=True)
            col2.write("<h2 class='metric_currency'>{}</h2>".format(currency), unsafe_allow_html=True)
            col3.write("<h2>{}</h2>".format(total_expenditure), unsafe_allow_html=True)
            col4.write("<h3 class='metric_name'>Expenditure</h3>", unsafe_allow_html=True)
            st.divider()

        with st.container():
            col1, col2, col3, col4, = st.columns(4)
            col1.write("<h1>📈</h1>", unsafe_allow_html=True)
            profit_margin_class = "positive-profit" if gross_profit_margin > 0 else "negative-profit"
            col3.write("<h2 class='profit-margin {}'>{:.1f}%</h2>".format(profit_margin_class, gross_profit_margin), unsafe_allow_html=True)
            col4.write("<h3 class='metric_name'>Profit</h3>", unsafe_allow_html=True)
            st.divider()

        funds_data = [total_revenue, total_expenditure]
        try:
            funds_labels = ['Revenue', 'Expenditure']
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(funds_data, labels=funds_labels, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle
            st.pyplot(fig)
        except:
            st.warning("There is no data to display charts. Please select a different date.")


    with page_col2:
        with st.container():
            col1, col2, col3, col4, = st.columns(4)
            col1.write("<h1>🏦</h1>", unsafe_allow_html=True)
            col2.write("<h2 class='metric_currency'>{}</h2>".format(currency), unsafe_allow_html=True)
            col3.write("<h2>{}</h2>".format(cash_reserves), unsafe_allow_html=True)
            col4.write("<h3 class='metric_name'>Cash Reserves</h3>", unsafe_allow_html=True)
            st.divider()

        with st.container():
            col1, col2, col3, col4, = st.columns(4)
            col1.write("<h1>🔥</h1>", unsafe_allow_html=True)
            col2.write("<h2 class='metric_currency'>{}</h2>".format(currency), unsafe_allow_html=True)
            col3.write("<h2>{}</h2>".format(burn_rate), unsafe_allow_html=True)
            col4.write("<h3 class='metric_name'>Burn Rate</h3>", unsafe_allow_html=True)
            st.divider()

    # # Graphs section (you can add your graph code here)
    # with col2:
    #     projection_df = create_5_year_projection(df)

    #     # # Display the 5-year projection DataFrame
    #     # st.subheader('5-Year Projection DataFrame')
    #     # st.write(projection_df)

    #     # Create a histogram of Monthly Revenue vs Expenses
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     sns.barplot(x='Date', y='Revenue', data=projection_df, color='blue', label='Revenue', ax=ax)
    #     sns.barplot(x='Date', y='Expenses', data=projection_df, color='red', label='Expenses', ax=ax)
    #     plt.title('Monthly Revenue vs Expenses - 5-Year Projection')
    #     plt.xlabel('Date')
    #     plt.ylabel('Amount')
    #     plt.xticks(rotation=45)
    #     st.subheader('5-Year Projection: Monthly Revenue vs Expenses')
    #     st.pyplot(fig)


if __name__ == "__main__":
    main()