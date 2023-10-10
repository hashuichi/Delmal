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
        name = st.text_input("Name", key="col1")
    with col2:
        cost = st.text_input("Cost", key="col2")
    with col3:
        price = st.text_input("Price", key="col3")
    with col4:
        quantity = st.text_input("Quantity Sold", key="col4")

    # Add the entered data to the session state data
    if st.button("Add"):
        st.session_state.data.append([name, cost, price, quantity])

    # Display the data in a dynamic table with a maximum of 10 rows
    st.title("Products:")
    df = pd.DataFrame(st.session_state.data[:10], columns=["Name", "Cost", "Price", "Quantity"])
    st.dataframe(df, width=800)

if __name__ == "__main__":
    main()