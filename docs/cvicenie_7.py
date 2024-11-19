import streamlit as st
import pandas as pd

def cvicenie_7():
    st.subheader('Začiatky knižnice Pandas a grafy')
    st.write('Imortovanie knižnice')
    st.code('''import pandas as pd''')
    with st.expander('Načítanie dataframu pomocou Dictionary'):

        dataframe = pd.DataFrame([
            {"price": 52.5, "quantity": 80},
            {"price": 50, "quantity": 100},
            {"price": 41, "quantity": 600},
            {"price": 30, "quantity": 150},
            {"price": 26, "quantity": 350}
        ])
        st.code('''
            dataframe = pd.DataFrame([
            {"price": 52.5, "quantity": 80},
            {"price": 50, "quantity": 100},
            {"price": 41, "quantity": 600},
            {"price": 30, "quantity": 150},
            {"price": 26, "quantity": 350}
        ])
        ''')
        st.write(dataframe)
    with st.expander('Práca s dataframe-om'):

        st.subheader("Zobrazenie jedného stĺpca")
        st.code('''dataframe['price']''')
        st.write(dataframe['price'])
        st.code('''dataframe[['price']]''')
        st.write(dataframe['price'])

        st.subheader('Zobrazenie viacerých stĺpcov')
        st.code('''dataframe[['price', 'quantity']]''')
        st.write(dataframe[['price', 'quantity']])

        st.subheader('Vytvorenie nového stĺpca')
        st.code('''dataframe['total_price'] = dataframe['price'] * dataframe['quantity']''')
        dataframe['total_price'] = dataframe['price'] * dataframe['quantity']
        st.write(dataframe)

        st.subheader('Výpočet priemerov pre každý stĺpec')
        st.code('''dataframe.mean()''')
        st.write(dataframe.mean())

        st.subheader('Súčet quantity')
        st.code('''dataframe['quantity'].sum()''')
        st.write(dataframe['quantity'].sum())

        st.subheader('Súčet quantít a celkovej ceny')
        st.code('''dataframe[['quantity', 'total_price']].sum()''')
        st.write(dataframe[['quantity', 'total_price']].sum())

        st.subheader('Funkcia describe')
        st.code('''dataframe.describe()''')
        st.write(dataframe.describe())

    with st.expander('Načítanie dataframu zo súboru'):

        st.code('''df = pd.read_excel('/content/energy-charts_Public_net_electricity_generation_in_Germany_in_2024.xlsx')''')
        df = pd.read_excel('docs/energy-charts_Public_net_electricity_generation_in_Germany_in_2024.xlsx')
        st.write(df)

        st.write('Ďalšie príklady')
        st.code('''
            pd.read_csv('data.csv')
            pd.read_json('data.json')
        ''')

    with st.expander('Lineárna regresia Residual Load'):
        st.write('zostávajúci dopyt po elektrickej energii, ktorý obnoviteľné zdroje energie nedokážu pokryť.')
        st.subheader('Vytvorenie dataframe-u data, vyberáme iba stĺpce, ktoré potrebujeme')
        st.code('''
            data = df[['Date (GMT+1)', 'Residual load', 'Day Ahead Auction (DE-LU)']]
            data = data.dropna()
            data
            ''')
        data = df[['Date (GMT+1)', 'Residual load', 'Day Ahead Auction (DE-LU)']]
        data = data.dropna()
        st.write(data)
        st.subheader('Zobrazenie scatter grafu')
        st.write('x os je Residual Load, y os je Day Ahead Auction (DE-LU)')
        st.code(
            '''
                plt.scatter(data[['Residual load']], data[['Day Ahead Auction (DE-LU)']], s=2)
                plt.show()
            '''
        )
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 4))
        plt.scatter(data[['Residual load']], data[['Day Ahead Auction (DE-LU)']], s=2)
        st.pyplot(plt.gcf(), use_container_width=False)

        st.subheader('Lineárna regresia')
        st.write('Importovanie LinearRegresion')
        st.code('''from sklearn.linear_model import LinearRegression''')
        from sklearn.linear_model import LinearRegression
        st.subheader('Vytvorenie a trénovanie modelu')
        st.code(
            '''
                model = LinearRegression()
                model.fit(data[['Residual load']], data[['Day Ahead Auction (DE-LU)']])
            '''
        )

        model = LinearRegression()
        model.fit(data[['Residual load']], data[['Day Ahead Auction (DE-LU)']])

        st.subheader('Vytvorenie predikcií')
        st.code('''y_pred = model.predict(data[['Residual load']])''')
        y_pred = model.predict(data[['Residual load']])
        st.subheader('Zobrazebie priamky v grafe lineárnej regresie')
        st.code(
            '''
                plt.figure(figsize=(10, 7))
                plt.scatter(data[['Residual load']], data[['Day Ahead Auction (DE-LU)']], s=1, color='blue')
                plt.plot(data[['Residual load']], y_pred, linewidth=0.8, color='red')
                plt.show()
            '''
        )
        plt.figure(figsize=(8, 4))
        plt.scatter(data[['Residual load']], data[['Day Ahead Auction (DE-LU)']], s=1, color='blue')
        plt.plot(data[['Residual load']], y_pred, linewidth=0.8, color='red')
        st.pyplot(plt.gcf(), use_container_width=False)

        st.subheader('Zobrazenie reálnych hodnôt a predikcií v čase')
        st.code(
            '''
                plt.figure(figsize=(50, 10))
                plt.plot(data['Date (GMT+1)'][-2000:], y_pred[-2000:], color='red', linewidth=0.6)
                plt.plot(data['Date (GMT+1)'][-2000:], data[['Day Ahead Auction (DE-LU)']][-2000:], color='blue', linewidth=0.6)
            '''
        )




        plt.figure(figsize=(50, 10))
        plt.plot(data['Date (GMT+1)'][-2000:], y_pred[-2000:], color='red', linewidth=0.6)
        plt.plot(data['Date (GMT+1)'][-2000:], data[['Day Ahead Auction (DE-LU)']][-2000:], color='blue', linewidth=0.6)
        st.pyplot(plt.gcf())

        st.subheader('Mean Square Error (MSE)')
        st.write('importovanie funkcie MSE')
        st.code('''from sklearn.metrics import mean_squared_error''')
        st.write('''Výpočet MSE''')

        from sklearn.metrics import mean_squared_error
        st.code('''
        mse = mean_squared_error(data[['Day Ahead Auction (DE-LU)']], y_pred)
        mse
        ''')
        mse = mean_squared_error(data[['Day Ahead Auction (DE-LU)']], y_pred)
        st.write(mse)

