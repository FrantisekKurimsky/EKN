import streamlit as st
from urllib.parse import urlencode, parse_qs

def get_slide_index():
    query_params = st.experimental_get_query_params()
    if "slide" in query_params:
        return int(query_params["slide"][0])
    return 0

# Function to set the current slide index in the URL
def set_slide_index(slide_index):
    st.experimental_set_query_params(slide=slide_index)


st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie-1"])

def home_page():
    st.title("Ekonomika v elektroenergetike")
    st.title("Cvičenia")

    
def first():
    slide_index = get_slide_index()
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
    st.title("Math Problem Slides")
    
    
    # Display the current math problem and solution
    problem = math_problems[slide_index]
    
    st.write(f"Príklad: 1.0{PROBLEM+1}")
    st.latex(problem["question"])
    
    with st.expander("Riešenie"):
        st.latex(problem["solution"])
    
    # Create navigation buttons for slides
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("Previous"):
            if slide_index > 0:
                set_slide_index(slide_index - 1)
    
    with col3:
        if st.button("Next"):
            if slide_index < len(math_problems) - 1:
                set_slide_index(slide_index + 1)
    
    st.write(f"Slide {slide_index + 1} of {len(math_problems)}")


# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "Cvičenie-1":
    first()