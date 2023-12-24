import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    data_path = "data.csv"
    explorer = DataExplorer(data_path)
    st.title("Data")
    explorer.date_selector()
    st.subheader("Enter New Data")
    explorer.input_data()
    explorer.load_data()

class DataExplorer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(data_path)
        self.filtered_data = None
        self.year = None
        self.month = None
        self.years_select = [2023,2024,2025,2026]
        self.months_select = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.new_entry = {'Name': None, 'Cost': None, 'Price': None, 'Quantity': None}

    def input_data(self):
        col1, col2, col3, col4 = st.columns(4)

        self.new_entry['Name'] = col1.text_input("Name", key="name")
        self.new_entry['Cost'] = col2.number_input("Cost", key="cost")
        self.new_entry['Price'] = col3.number_input("Price", key="price")
        self.new_entry['Quantity']= col4.number_input("Quantity Sold", key="quantity", step=1)
                
        if st.button("Add", type='primary', use_container_width=True):
            self.new_entry['Year'] = self.year
            self.new_entry['Month'] = self.month

             # Check if an entry with the same name, year, and month exists
            existing_entry_index = (self.data['Name'] == self.new_entry['Name']) & \
                                   (self.data['Year'] == self.new_entry['Year']) & \
                                   (self.data['Month'] == self.new_entry['Month'])

            if existing_entry_index.any():
                # Update existing entry
                self.data.loc[existing_entry_index, ['Cost', 'Price', 'Quantity']] = \
                    self.new_entry['Cost'], self.new_entry['Price'], self.new_entry['Quantity']
            else:
                # Append new entry to the data file
                self.data = pd.concat([self.data, pd.DataFrame([self.new_entry])], ignore_index=True)

            # self.data.loc[len(self.data)] = self.new_entry
            self.data.to_csv(self.data_path, index=False)
            self.new_entry = {'Name': None, 'Cost': None, 'Price': None, 'Quantity': None}

    def load_data(self):
        self.filtered_data = self.data[(self.data['Year'] == self.year) & (self.data['Month'] == self.month)]
        self.filtered_data = self.filtered_data.drop(columns=['Year','Month'])
        self.filtered_data.reset_index(drop=True, inplace=True)
        st.subheader(f"Data for {self.month} {self.year}")
        st.write(self.filtered_data)

    def date_selector(self):
        col1, col2 = st.columns(2)
        self.year = col1.selectbox("Select Year", self.years_select)
        self.month = col2.selectbox("Select Month", self.months_select)

if __name__ == "__main__":
    main()