import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def cvicenie_8():

    st.write('Importovanie knižnice pandas')
    st.code('''import pandas as pd''')
    st.write('Stiahneme si dáta z https://www.energy-charts.info/charts/price_spot_market/chart.htm?l=en&c=NL&interval=year&legendItems=7y5  \n vymažeme nežiadúce riadky, v našom prípade 1. a 3. a nahráme do prostredia colab')
    st.code('''
        df = pd.read_excel("/content/energy-charts_Electricity_production_and_spot_prices_the_Netherlands_in_2024.xlsx")
        df
    ''')
    df = pd.read_excel("docs/energy-charts_Electricity_production_and_spot_prices_the_Netherlands_in_2024.xlsx")
    st.write(df)

    st.write('Z dataframu odstránime riadky, kde nám chýbajú hodnoty')
    st.code('''
        df.dropna(inplace=True)
        df
    ''')
    df.dropna(inplace=True)
    st.write(df)

    st.write('Pozrieme sa, kedy sa jedná o negatívnu cenu')
    st.code('''df['Day Ahead Auction (NL)'] < 0''')
    st.write(df['Day Ahead Auction (NL)'] < 0)
    st.write('Následne vieme spraviť kumulatívny súčet, koľko krát sa vyskytla negatívna cena')
    st.code('''(df['Day Ahead Auction (NL)'] < 0).cumsum()''')
    st.write((df['Day Ahead Auction (NL)'] < 0).cumsum())

    st.write('Toto si vieme pridať do pôvodného dataframu, vytvoríme nový stĺpec, kde pridáme kumulatívny počet negatívnych cien')
    st.code('''
        df['Cumulative count of negative prices'] = (df['Day Ahead Auction (NL)'] < 0).cumsum()
        df
    ''')
    df['Cumulative count of negative prices'] = (df['Day Ahead Auction (NL)'] < 0).cumsum()
    st.write(df)

    st.write('Importovanie knižnice matplotlib')
    st.code('''import matplotlib.pyplot as plt''')

    st.write('Vykreslenie grafu, x-ová os je Dátum, y-ová os je kumulatívny počet negatívnych cien')
    st.code('''
        plt.plot(df['Date (GMT+1)'], df['Cumulative count of negative prices'], linestyle='-')
        plt.show()
    ''')
    plt.figure(figsize=(30, 10))
    plt.plot(df['Date (GMT+1)'], df['Cumulative count of negative prices'], linestyle='-')
    st.pyplot(plt.gcf())