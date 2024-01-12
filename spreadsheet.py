import streamlit as st
import pandas as pd
from datetime import datetime

class Spreadsheet:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(data_path)
        self.filtered_data = None
        self.selected_date = None
        self.new_entry = {}

    def input_data(self):
        col1, col2, col3, col4, col5 = st.columns([2,2,2,2,0.7])

        self.new_entry['Name'] = col1.text_input("Name", key="name", label_visibility="collapsed")
        self.new_entry['Cost'] = col2.number_input("Cost", key="cost", label_visibility="collapsed")
        self.new_entry['Price'] = col3.number_input("Price", key="price", label_visibility="collapsed")
        self.new_entry['Quantity']= col4.number_input("Quantity Sold", key="quantity", step=1, label_visibility="collapsed")
                
        if st.button("Add", type='primary', use_container_width=True):
            self.new_entry['Date'] = self.selected_date
            self.data = pd.concat([self.data, pd.DataFrame([self.new_entry])], ignore_index=True)
            self.data.to_csv(self.data_path, index=False)
            self.new_entry = {'Name': None, 'Cost': None, 'Price': None, 'Quantity': None}
            st.success(f"Added New Entry")  

    def load_data(self):
        self.filtered_data = self.data[self.data['Date'] == self.selected_date.strftime("%Y-%m-%d")]
        self.filtered_data = self.filtered_data.drop(columns='Date')
        self.original_indices = self.filtered_data.index.tolist()
        self.filtered_data.reset_index(drop=True, inplace=True)

        # st.subheader(f"Data for {self.selected_date}")
        num_columns = self.filtered_data.shape[1]
        column_widths = [2] * (num_columns) + [0.6]
        columns = st.columns(column_widths)

        for i, col in enumerate(columns):
            if i == num_columns:
                col.write("**Delete**")
            else:
                col.write(f"**{self.filtered_data.columns[i]}**")


        if self.filtered_data.empty:
            for i, col in enumerate(columns):
                col.write("No Data")
        else:
            for index, row in self.filtered_data.iterrows():
                columns = st.columns(column_widths)
                for i, col in enumerate(columns):
                    if i == num_columns:
                        if columns[-1].button(":x:", key=f"delete_{index}"):   
                            self.delete_row(index, row) 
                    else:
                        col.write(f"{row.iloc[i]}")

    def delete_row(self, index, row):
        original_index = self.original_indices[index]
        self.data = self.data.drop(index=original_index)
        self.data.to_csv(self.data_path, index=False)
        st.success(f"Deleted {row.iloc[0]}")  

    def date_selector(self):
        self.selected_date = st.date_input("Select Date", min_value=datetime(2020, 1, 1), max_value=datetime.now())