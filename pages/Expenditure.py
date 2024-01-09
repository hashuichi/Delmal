import streamlit as st
import pandas as pd
from datetime import datetime
from spreadsheet import Spreadsheet

def main():
    data_path = "expenditure.csv"
    explorer = Spreadsheet(data_path)
    st.title("Data")
    explorer.date_selector()
    explorer.load_data()
    explorer.input_data()

if __name__ == "__main__":
    main()