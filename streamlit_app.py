import streamlit as st
from urllib.parse import urlencode, parse_qs
import pandas as pd
from problems import math_problems_1



st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie 1."])

def home_page():
    st.title("Ekonomika v elektroenergetike")
    st.title("Cvičenia")
    col1, col2, col3 = st.columns(3)

    # Button for Cvičenie 1
    with col1:
        if st.button("Cvičenie 1."):
            st.session_state.page = "Cvičenie 1."

    
def first():
    

    st.title("Cvičenie 1.")

    slide_index = st.selectbox(
        "Príklad:",
        list(range(len(math_problems_1))),
        format_func=lambda x: f"Príklad: 1.{x+1}"
    )
    
    
    # Display the current math problem and solution
    problem = math_problems_1[slide_index]
    
    st.write(problem["question"])
    if problem['table'] is not None:
        st.write(problem['table'])
    
    with st.expander("Riešenie"):
        st.latex(problem["solution"])

        if problem['code'] is not None:
            example = problem['code']
            result = eval(example)
            # st.write(example)
            st.latex(str(result))



# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "Cvičenie 1." or st.session_state.page == "Cvičenie 1.":
    first()
