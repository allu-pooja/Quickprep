import streamlit as st
from login import login_page
from quickprep import quickprep_page

if "authenticated" not in st.session_state:
    st.session_state["authenticated"]=False

if st.session_state["authenticated"]:
    quickprep_page()

else:
    login_page()