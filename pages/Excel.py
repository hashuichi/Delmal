import streamlit as st

st.header("My Demo App")

if 'open' not in st.session_state:
            st.session_state.open = False

button_a = st.button('Import Excel')
if button_a:
    st.session_state.open = not st.session_state.open
if st.session_state.open:
    uploaded_file = st.file_uploader("**Import from Excel**", type=["xlsx", "xls"], label_visibility="hidden")

