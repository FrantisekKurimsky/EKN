import streamlit as st
from urllib.parse import urlencode, parse_qs

math_problems = [
    {
        "question": r"\text{Solve for } x \text{ in the equation:} \ ax^2 + bx + c = 0",
        "solution": r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"
    },
    {
        "question": r"\text{Find the derivative of:} \ f(x) = 3x^3 + 2x^2 - 5x + 1",
        "solution": r"f'(x) = 9x^2 + 4x - 5"
    },
    {
        "question": r"\text{Evaluate the integral:} \ \int_0^1 x^2 \, dx",
        "solution": r"\frac{1}{3}"
    },
]


st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie-1"])

def home_page():
    st.title("Ekonomika v elektroenergetike")
    st.title("Cvičenia")

    
def first():
    slide_index = st.radio(
        "Select a math problem:",
        list(range(len(math_problems))),
        format_func=lambda x: f"Problem {x + 1}"
    )

    st.title("Math Problem Slides")
    
    
    # Display the current math problem and solution
    problem = math_problems[slide_index]
    
    st.write(f"Príklad: 1.0{slide_index+1}")
    st.latex(problem["question"])
    
    with st.expander("Riešenie"):
        st.latex(problem["solution"])
    
    # Create navigation buttons for slides
    col1, col2, col3 = st.columns([1, 2, 1])
    
    st.write(f"Slide {slide_index + 1} of {len(math_problems)}")


# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "Cvičenie-1":
    first()