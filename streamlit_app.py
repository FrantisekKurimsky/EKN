import streamlit as st



st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie-1"])

def home_page():
    st.title("Ekonomika v elektroenergetike")
    st.title("Cvičenia")

    
def first():
    PROBLEM = 0
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
    problem = math_problems[PROBLEM]
    
    st.write("Problem:")
    st.latex(problem["question"])
    
    with st.expander("Solution"):
        st.latex(problem["solution"])
    
    # Create navigation buttons for slides
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("Previous"):
            if PROBLEM > 0:
                PROBLEM -= 1
            
    
    with col3:
        if st.button("Next"):
            if PROBLEM < len(math_problems) - 1:
                PROBLEM += 1
    
    st.write(f"Slide {PROBLEM + 1} of {len(math_problems)}")


# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "Cvičenie-1":
    first()