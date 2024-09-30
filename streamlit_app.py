import streamlit as st
from urllib.parse import urlencode, parse_qs
import pandas as pd

math_problems_1 = [
    {
        "question": "Banka poskytuje 11 % ročný úrok na uložených vkladoch. Banka pripisuje úroky v poslednom dni každého štvrťroka. Peniaze uložené na vklad sa úročia na bežný mesiac, ak sú vložené do 8. dňa v bežnom mesiaci. Občan si otvoril účet 8. januára a vložil 5000 €. Aký veľký úrok získa do 30. júna?",
        "solution": r"\text{základ úrokovania: } r=1+i=1+p/100, \\ p: \text{percentová úroková miera a } i: \text{úroková sadzba} \\ \text{__________} \\ u=K_0⋅i⋅nu=K_0⋅i⋅n",
        "table": None
    },
    {
        "question": "Banka poskytuje na vkladoch 8 % ročný úrok. Karol potrebuje za 9 mesiacov vrátiť dlžobu 5000 €. Koľko musí  teraz vložiť do banky, aby mal za 9 mesiacov k dispozícii práve túto sumu?",
        "solution": r"f'(x) = 9x^2 + 4x - 5",
        "table": None
    },
    {
        "question": "Helena investovala 5000 € na zamestnanecký účet, ktorý prináša 8 % ročný úrok. Ako dlho má ponechať túto sumu na účte, aby získala 300€?",
        "solution": r"\frac{1}{3}",
        "table": None
    },
    {
        "question": "Inštalovaný výkon modelovej elektrizačnej sústavy je koncom roka 2009  Pi = 234 GW. Aký veľký inštalovaný výkon bude mať táto sústava roku 2015, ak predpokladáme každoročný vzrast inštalovaného výkonu o 6%?",
        "solution": r"\frac{1}{3}",
        "table": None
    },
    {
        "question": "Na účely budúcej investičnej výstavby začiatkom roku 2010 ukladá podnik do banky podľa dlhodobého finančného plánu na konci uvedených rokov čiastky podľa nasledujúcej tabuľky. Akú  čiastku bude mať podnik k dispozícii pri začatí výstavby, ak úroková miera p=6%?",
        "table": pd.DataFrame({
            "Rok": [int(x) for x in [2000, 2001, 2002, 2004, 2006, 2008]],
            "K (mil. Eur)": [3.8, 4.1, 3.6, 3.9, 4.0, 3.7]
        }).T,
        "solution": r"\frac{1}{3}"
    },
    {
        "question": "Rozhodnite, o aký investičný úver má dnes požiadať podnik banku, aby pri úrokovej miere p = 6% mohol tento úver práve splatiť po 9 rokoch predpokladanými voľnými finančnými zdrojmi (odpismi a časťou zisku), ktoré sa budú podľa dlhodobého plánu podniku tvoriť tak, ako je vidieť z nasledujúcej tabuľky:",
        "solution": r"\frac{1}{3}",
        "table": pd.DataFrame({
            "Rok": [int(x) for x in [1, 2, 4, 6, 8, 9]],
            "K (mil. Eur)": [13, 15, 16, 17, 18, 17]
        }).T,

    },
]


st.sidebar.title("Menu")
pages = st.sidebar.radio("", ["Domov", "Cvičenie-1"])

def home_page():
    st.title("Ekonomika v elektroenergetike")
    st.title("Cvičenia")

    
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


# Navigation logic
if pages == "Domov":
    home_page()
elif pages == "Cvičenie-1":
    first()