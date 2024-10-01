import streamlit as st
from urllib.parse import urlencode, parse_qs
import pandas as pd
from problems import math_problems_1

st.set_page_config(layout="wide")
st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie 1."])

def home_page():
    st.title("Ekonomika v elektroenergetike")


    
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
elif pages == "Cvičenie 1.":
    first()