import streamlit as st
import streamlit_nested_layout
from PIL import Image
from docs.cvicenie_7 import cvicenie_7
from docs.cvicenie_6 import cvicenie_6
from docs.cvicenie_8 import cvicenie_8
import pandas as pd
from problems import (
    math_problems_1,
    math_problems_2,
    math_problems_3,
)
from streamlit_pdf_viewer import pdf_viewer
import streamlit.components.v1 as components

st.set_page_config(layout="wide")



st.sidebar.title("Menu")
# MENU
pages = st.sidebar.selectbox("", ["Domov", "Cvičenie 1.", "Cvičenie 2.", "Cvičenie 3.", "Cvičenie 4. a 5.", "Cvičenie 6.", "Cvičenie 7.", "Cvičenie 8."])

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
        if 'a' in problem['table']:
            st.write('a)')
            st.write(problem['table']['a'])
        if 'b' in problem['table']:
            st.write('b)')
            st.write(problem['table']['b'])
        if isinstance(problem['table'], pd.DataFrame):
            st.write(problem['table'])
    if "video" in problem:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.video(problem['video'])

    with st.expander("Riešenie"):
        if problem["solution"] is not None:
            st.latex(problem["solution"])

        if problem['code'] is not None:
            example = problem['code']
            result = eval(example)
            # st.write(example)
            if result is not None:
                st.latex(str(result))
        
        if problem['solutiontable'] is not None:
            if 'a' in problem['solutiontable']:
                st.write('a)')
                st.write(problem['solutiontable']['a'])
            if 'b' in problem['solutiontable']:
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
elif pages == "Cvičenie 3.":
    first("Cvičenie 3.", math_problems_3, 3)
elif pages == "Cvičenie 4. a 5.":
    st.title("Cvičenie 4. a 5.")
    pdf_viewer("docs/cv_4_5.pdf", width=800, pages_vertical_spacing=3, resolution_boost=2)
elif pages == "Cvičenie 6.":
    st.title("Cvičenie 6.")
    file_path = "docs/Cvicenie_6.ipynb"


    with open(file_path, "rb") as file:
        notebook_content = file.read()

    # Create a download button
    st.download_button(
        label="Stiahnuť Jupyter Notebook",
        data=notebook_content,
        file_name="Cvicenie_6.ipynb",
        mime="application/octet-stream"
    )

    st.write('Súbor si môžete stiahnúť a otvoriť v prostredí colab, cez File/Upload notebook.')
    image = Image.open("docs/Screenshot 2024-11-11 172149.png")
    st.image(image, caption="Image Loaded with PIL", use_column_width=False)
    cvicenie_6()

elif pages == "Cvičenie 7.":
    st.title("Cvičenie 7.")
    st.subheader('Sledovanie závislosti medzi cenami elektriny a Residual Load pre Nemecko')
    file_path = "docs/Cvicenie_7.ipynb"
    with open(file_path, "rb") as file:
        notebook_content = file.read()

    # Create a download button
    st.download_button(
        label="Stiahnuť Jupyter Notebook",
        data=notebook_content,
        file_name="Cvicenie_7.ipynb",
        mime="application/octet-stream"
    )
    with st.expander('MatPlotLib Graphs'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image('docs/MatPlotLib.png')

    with st.expander('Linear Regression'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.video('https://www.youtube.com/watch?v=PGXI9UzaKfA')

    with st.expander('Mean square error (MSE)'):

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image('docs/MSE.png')
    st.write('Odkazy')
    st.write('https://www.energy-charts.info/?l=en&c=DE')
    st.write('tutorial pandas https://www.w3schools.com/python/pandas/pandas_dataframes.asp')
    st.write('tutorial matplotlib https://www.w3schools.com/python/matplotlib_intro.asp')

    cvicenie_7()

elif pages == "Cvičenie 8.":
    st.title('Cvicenie 8')
    st.subheader('Sledovanie negatívnych cien v Holandsku pre rok 2024')
    file_path = "docs/Cvicenie_8.ipynb"
    with open(file_path, "rb") as file:
        notebook_content = file.read()

    # Create a download button
    st.download_button(
        label="Stiahnuť Jupyter Notebook",
        data=notebook_content,
        file_name="Cvicenie_8.ipynb",
        mime="application/octet-stream"
    )
    cvicenie_8()
