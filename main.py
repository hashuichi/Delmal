import streamlit as st
import pandas as pd

# Define the Streamlit app
def main():
    # Set the title of the app
    st.title("Financial Model")

    # Initialize or get the data from the session state
    if 'data' not in st.session_state:
        st.session_state.data = []

    st.markdown(
        """
        <style>
        .stTextInput {
            width: 100%;
        }
        .stButton button {
            width: 100%;
        }
        .input-col {
            display: flex;
        }
        .input-col .stTextInput {
            flex: 1;
        }
        .input-col .stButton {
            flex: 0;
            margin-left: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create a grid with 4 columns
    col1, col2, col3, col4 = st.columns(4)

    # Create input fields in each column
    with col1:
        name = st.text_input("Name", key="name")
    with col2:
        cost = st.number_input("Cost", key="cost")
    with col3:
        price = st.number_input("Price", key="price")
    with col4:
        quantity_sold = st.number_input("Quantity Sold", key="quantity_sold", step=1)

    # Add the entered data to the session state data
    if st.button("Add"):
        if len(st.session_state.data) < 10:
            st.session_state.data.append([name, cost, price, quantity_sold])
        else:
            st.warning("You have reached the maximum of 10 rows and cannot add more.")

    # Display the data in a dynamic table with a maximum of 10 rows
    st.title("Products:")
    df = pd.DataFrame(st.session_state.data[:10], columns=["Name", "Cost", "Price", "Quantity Sold"])

    # Calculate Revenue and Profit
    df['Revenue'] = df['Price'] * df['Quantity Sold']
    df['Profit'] = (df['Price'] - df['Cost']) * df['Quantity Sold']

    st.dataframe(df, width=800)

    # Calculate and display the total Revenue and Profit
    total_revenue = df['Revenue'].sum()
    total_profit = df['Profit'].sum()
    st.write(f"Total Revenue: £{total_revenue:.2f}")
    st.write(f"Total Profit: £{total_profit:.2f}")

    # Input field for initial investment
    investment = st.number_input("Investment", key="investment", min_value=0, step=1)
    roi = (total_profit / investment) * 100 if investment > 0 else 0
    st.write(f"Return on Investment (ROI): {roi:.2f}%")

if __name__ == "__main__":
    main()