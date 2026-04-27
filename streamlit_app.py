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

# Import new modular pages
from pages.uploads import upload_page, results_page
from pages.merit_order import merit_order_page
# from pages.contest import contest_page
from pages.prediction import predict_page
from pages.final_assignment_data import final_assignment_data_page
from pages.final_assignment_submission import (
    final_assignment_brief_page,
    final_assignment_upload_page,
    final_assignment_results_page,
)
from utils.auth import require_login_for_protected_pages, show_logout_button

st.set_page_config(layout="wide")

HERO_IMAGE_URL = (
    "./docs/placeholder.png"
)


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


def _home_page():
    st.title("Ekonomika v elektroenergetike")


    st.image(
        HERO_IMAGE_URL,
        use_container_width=True,
    )

    st.markdown("---")

    logo_cols = st.columns(3, gap="large")
    logo_cards = [
        (
            "https://upload.wikimedia.org/wikipedia/commons/5/54/TUKE_logo.jpg",
            "https://www.tuke.sk",
            "Technická univerzita v Košiciach",
        ),
        (
            "https://kee.fei.tuke.sk/wp-content/uploads/2020/01/logo2-e1579263774637.png",
            "https://kee.fei.tuke.sk",
            "Katedra elektroenergetiky",
        ),
        (
            "https://epic.tuke.sk/assets/EP_Innovation_Centre_RGB-SIjXd0Eb.jpg",
            "https://epic.tuke.sk",
            "EPIC",
        ),
    ]

    for column, (image_url, target_url, label) in zip(logo_cols, logo_cards):
        with column:
            st.markdown(
                f'''
                <a href="{target_url}" target="_blank" style="text-decoration:none;">
                    <div style="
                        border: 1px solid rgba(0,0,0,0.08);
                        border-radius: 14px;
                        padding: 16px;
                        background: white;
                        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
                        min-height: 190px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <img src="{image_url}" alt="{label}" style="max-width: 100%; max-height: 130px; object-fit: contain;" />
                    </div>
                </a>
                ''',
                unsafe_allow_html=True,
            )

def _exercise_1_page():
    _display_problem("Cvičenie 1.", math_problems_1, 1)


def _exercise_2_page():
    _display_problem("Cvičenie 2.", math_problems_2, 2)


def _exercise_3_page():
    _display_problem("Cvičenie 3.", math_problems_3, 3)


def _exercise_4_5_page():
    st.title("Cvičenie 4. a 5.")
    pdf_viewer("docs/cv_4_5.pdf", width=800, pages_vertical_spacing=3, resolution_boost=2)


def _exercise_6_page():
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
    st.image(image, caption="Image Loaded with PIL", width='content')
    cvicenie_6()


def _exercise_7_page():
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


def _exercise_8_page():
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


def _upload_page_protected():
    if require_login_for_protected_pages():
        upload_page()


def _final_assignment_upload_page_protected():
    if require_login_for_protected_pages():
        final_assignment_upload_page()


navigation = st.navigation(
    {
        "Výučba": [
            st.Page(_home_page, title="Domov", icon="🏠", url_path="", default=True),
            st.Page(_exercise_1_page, title="Cvičenie 1", icon="1️⃣", url_path="cvicenie-1"),
            st.Page(_exercise_2_page, title="Cvičenie 2", icon="2️⃣", url_path="cvicenie-2"),
            st.Page(_exercise_3_page, title="Cvičenie 3", icon="3️⃣", url_path="cvicenie-3"),
            st.Page(_exercise_4_5_page, title="Cvičenie 4 a 5", icon="4️⃣", url_path="cvicenie-4-5"),
            st.Page(_exercise_6_page, title="Cvičenie 6", icon="6️⃣", url_path="cvicenie-6"),
            st.Page(_exercise_7_page, title="Cvičenie 7", icon="7️⃣", url_path="cvicenie-7"),
            st.Page(_exercise_8_page, title="Cvičenie 8", icon="8️⃣", url_path="cvicenie-8"),
            st.Page(merit_order_page, title="Merit Order", icon="⚡", url_path="merit-order"),
            st.Page(
                predict_page,
                title="Predikcia veternej energie",
                icon="🌬️",
                url_path="predikcia-veterna-energia",
            ),
        ],
        "Výsledky z cvičení": [
            st.Page(_upload_page_protected, title="Odovzdanie výsledkov", icon="📤", url_path="odovzdanie"),
            st.Page(results_page, title="Prehľad výsledkov", icon="📋", url_path="vysledky"),
        ],
        "Záverečné zadanie": [
            st.Page(
                final_assignment_brief_page,
                title="Zadanie a pokyny",
                icon="📘",
                url_path="zaverecne-zadanie-pokyny",
            ),
            st.Page(
                final_assignment_data_page,
                title="Získanie dát",
                icon="📡",
                url_path="zaverecne-zadanie-ziskanie-dat",
            ),
            # st.Page(
            #     _final_assignment_upload_page_protected,
            #     title="Odovzdanie zadania",
            #     icon="📤",
            #     url_path="zaverecne-zadanie-odovzdanie",
            # ),
            # st.Page(
            #     final_assignment_results_page,
            #     title="Prehľad odovzdaní",
            #     icon="📊",
            #     url_path="zaverecne-zadanie-vysledky",
            # ),
        ],
    },
    position="top",
)

if st.session_state.get("is_authenticated"):
    show_logout_button()

navigation.run()