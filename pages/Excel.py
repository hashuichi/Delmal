import streamlit as st
import pandas as pd

st.header("My Demo App")

if 'open' not in st.session_state:
    st.session_state.open = False
if 'data' not in st.session_state:
    st.session_state.data = []

def toggle_excel():
    st.session_state.open = not st.session_state.open

st.button('Import Excel', on_click=toggle_excel)

if st.session_state.open:
    uploaded_file = st.file_uploader("**Import from Excel**", type=["xlsx", "xls"], label_visibility="hidden")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        selected_columns = st.multiselect("Select Columns", df.columns.tolist(), default=df.columns.tolist())
        st.session_state.data = df[selected_columns]
        st.button('Confirm', on_click=toggle_excel)

if len(st.session_state.data) > 0:
    st.write(st.session_state.data)

if st.button('Empty Data'):
    st.session_state.data = []