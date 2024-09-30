import streamlit as st



st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Domov", "1. Cvičenie"])

def home_page():
    st.title("Ekonomika v elektroenergetike - cvičenia")

# Function to display the Math Problem page
def first():
    st.title("Math Problem")
    st.write("Here is a math problem formatted using LaTeX:")
    
    # Display a simple LaTeX math problem
    st.latex(r'''
    \text{Solve for } x \text{ in the equation:}
    ax^2 + bx + c = 0
    ''')
    
    st.write("This is the quadratic equation. The solution is given by:")
    
    # Display the quadratic formula in LaTeX
    st.latex(r'''
    x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
    ''')

# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "1. Cvičenie":
    first()