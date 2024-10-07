import streamlit as st
from urllib.parse import urlencode, parse_qs
import pandas as pd
from problems import (
    math_problems_1,
    math_problems_2
)

st.set_page_config(layout="wide")
st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie 1.", "Cvičenie 2."])

def home_page():
    st.title("Ekonomika v elektroenergetike")


    
def first(name, problems, number):
    

    st.title(name)

    slide_index = st.selectbox(
        "Príklad:",
        list(range(len(problems))),
        format_func=lambda x: f"Príklad: {number}.{x+1}"
    )
    
    
    # Display the current math problem and solution
    problem = problems[slide_index]
    
    st.write(problem["question"])
    if problem['table'] is not None:
        if problem['table']['a'] is not None:
            st.write('a)')
            st.write(problem['table']['a'])
        if problem['table']['b'] is not None:
            st.write('b)')
            st.write(problem['table']['b'])
        if isinstance(problem['table'], pd.DataFrame):
            st.write(problem['table'])

    with st.expander("Riešenie"):
        st.latex(problem["solution"])

        if problem['code'] is not None:
            example = problem['code']
            result = eval(example)
            # st.write(example)
            st.latex(str(result))
        
        if problem['solutiontable'] is not None:
            if problem['solutiontable']['a'] is not None:
                st.write('a)')
                st.write(problem['solutiontable']['a'])
            if problem['solutiontable']['b'] is not None:
                st.write('b)')
                st.write(problem['solutiontable']['b'])
            if isinstance(problem['solutiontable'], pd.DataFrame):
                st.write(problem['solutiontable'])



# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "Cvičenie 1.":
    first("Cvičenie 1.", math_problems_1, 1)
elif pages == "Cvičenie 2.":
    first("Cvičenie 2.", math_problems_2, 2)