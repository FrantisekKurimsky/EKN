import streamlit as st
import streamlit_nested_layout
from PIL import Image
from docs.cvicenie_7 import cvicenie_7
from docs.cvicenie_6 import cvicenie_6
from docs.cvicenie_8 import cvicenie_8
import pandas as pd
from firebase_admin import firestore
from problems import (
    math_problems_1,
    math_problems_2,
    math_problems_3,
)
from streamlit_pdf_viewer import pdf_viewer

# Import new modular pages
from pages.uploads import upload_page, results_page
from pages.merit_order import merit_order_page
# from pages.contest import contest_page
from pages.prediction import predict_page
from utils.auth import require_login_for_protected_pages, show_logout_button

st.set_page_config(layout="wide")





st.sidebar.title("Menu")
exercise_pages = [
    "Domov",
    "Cvičenie 1.",
    "Cvičenie 2.",
    "Cvičenie 3.",
    "Cvičenie 4. a 5.",
    "Cvičenie 6.",
    "Cvičenie 7.",
    "Cvičenie 8.",
    "Merit Order",
    "Predikcia výroby veternej energie",  # New page for prediction
    # "Sutaz",
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Domov"
if "last_exercise_choice" not in st.session_state:
    st.session_state.last_exercise_choice = "Domov"

exercise_choice = st.sidebar.selectbox(
    "Select exercise",
    exercise_pages,
    index=exercise_pages.index(st.session_state.last_exercise_choice),
    label_visibility="collapsed",
)

if exercise_choice != st.session_state.last_exercise_choice:
    st.session_state.current_page = exercise_choice

st.session_state.last_exercise_choice = exercise_choice

st.sidebar.markdown("---")
st.sidebar.caption("Odovzdania")
if st.sidebar.button("Odovzdanie výsledkov", use_container_width=True):
    st.session_state.current_page = "Odovzdanie výsledkov"
    st.rerun()

if st.sidebar.button("Prehľad výsledkov", use_container_width=True):
    st.session_state.current_page = "Prehľad výsledkov"
    st.rerun()

pages = st.session_state.current_page


if st.session_state.get("is_authenticated"):
    show_logout_button()


def _display_problem(name, problems, number):
    """Display math problems with solutions."""
    st.title(name)

    slide_index = st.selectbox(
        "Príklad:",
        list(range(len(problems))),
        format_func=lambda x: f"Príklad: {number}.{x+1}"
    )
    
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
    st.title("Ekonomika v elektroenergetike")

elif pages == "Cvičenie 1.":
    _display_problem("Cvičenie 1.", math_problems_1, 1)
elif pages == "Cvičenie 2.":
    _display_problem("Cvičenie 2.", math_problems_2, 2)
elif pages == "Cvičenie 3.":
    _display_problem("Cvičenie 3.", math_problems_3, 3)
elif pages == "Cvičenie 4. a 5.":
    st.title("Cvičenie 4. a 5.")
    pdf_viewer("docs/cv_4_5.pdf", width=800, pages_vertical_spacing=3, resolution_boost=2)
elif pages == "Cvičenie 6.":
    st.title("Cvičenie 6.")
    file_path = "docs/Cvicenie_6.ipynb"
    with open(file_path, "rb") as file:
        notebook_content = file.read()
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
    st.download_button(
        label="Stiahnuť Jupyter Notebook",
        data=notebook_content,
        file_name="Cvicenie_8.ipynb",
        mime="application/octet-stream"
    )
    cvicenie_8()

elif pages == "Merit Order":
    merit_order_page()

# elif pages == "Sutaz":
#     contest_page()

elif pages == "Odovzdanie výsledkov":
    if require_login_for_protected_pages():
        upload_page()

elif pages == "Prehľad výsledkov":
    if require_login_for_protected_pages():
        results_page()

elif pages == "Predikcia výroby veternej energie":
    predict_page()
