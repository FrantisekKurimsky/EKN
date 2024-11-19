import streamlit as st
import math
def cvicenie_6():
    st.header('Základy Pythonu')
    with st.expander('Dátové typy'):
        with st.expander('Boolean - binárny typ (True alebo False)'):

            st.code("""
                boolean1 = True
                boolean2 = False
                
                display(
                    boolean1,
                    type(boolean1),
                    boolean2,
                    type(boolean2)
                )
            """)
            boolean1 = True
            boolean2 = False
            st.write(
                boolean1,
                str(type(boolean1)),
                boolean2,
                str(type(boolean2))
            )
            st.write('Logické operácie')
            st.code('''boolean1 and boolean1, boolean1 and boolean2, boolean2 and boolean2''')
            st.write(boolean1 and boolean1, boolean1 and boolean2, boolean2 and boolean2)
            st.code('''boolean1 or boolean1, boolean1 or boolean2, boolean2 or boolean2''')
            st.write(boolean1 or boolean1, boolean1 or boolean2, boolean2 or boolean2)
            st.code('''not boolean1, not boolean2''')
            st.write(not boolean1, not boolean2)

        with st.expander('Integer - číselný typ prezentovaný ako celé číslo'):
            st.code('''
            x = 2
            x, type(x)
            ''')

            x = 2
            st.write(x, str(type(x)))
            st.write('Operácie')
            st.code('''
                x += 1
                print(x)
                x -= 1
                print(x)
                x *= 2
                print(x)
                x /= 2
                print(x)
                x **= 2
                print(x)
            ''')
            x += 1
            st.write(x)
            x -= 1
            st.write(x)
            x *= 2
            st.write(x)
            x /= 2
            st.write(x)
            x **= 2
            st.write(x)

            st.code('''
                import math
                x = math.sqrt(x)
                x
            ''')
            x = math.sqrt(x)
            st.write(x)


            st.write('Zvyšok po delení, modulo')
            st.code('''25 % 4''')
            st.write(25 % 4)

        with st.expander('Float - číselný typ prezentovaný ako desatinné číslo'):
            st.code('''
                x = 2.36
                x, type(x)
            ''')

            x = 2.36
            st.write(x, str(type(x)))

        with st.expander('Reťazec(String) - Typ textu | Syntax - „text“'):

            st.code('''
            string = "KEE - Katedra Elektroenegetiky"
            string = 'KEE - Katedra Elektroenegetiky'
            print(string)
            type(string)
            ''')
            string = "KEE - Katedra Elektroenegetiky"
            st.write(string, str(type(string)))
            st.subheader('Operácie so stringom')
            st.code('''
            string1 = "some text"
            string2 = 'some other text'
            ''')
            st.subheader('Znak na danom indexe')

            string1 = "some text"
            string2 = 'some other text'
            st.code('''string1[3]''')
            st.write(string1[3])

            st.subheader('Získanie podreťazca')
            st.code('''string1[5:]''')
            st.write(string1[5:])

            st.subheader('Spojenie reťazcov')
            st.code('''
            display(string1 + " and " + string2)
            f'text {string1}'
            ''')

            st.write(string1 + " and " + string2)
            st.write(f'text {string1}')

            st.subheader('Všetky znaky veľké, malé, prvý znak veľký')
            st.code('''string.upper(), string.lower(), string.capitalize()''')
            st.write(string.upper(), string.lower(), string.capitalize())

            st.subheader('Počet znakov v reťazci')
            st.code('''len(string)''')
            st.write(len(string))

        with st.expander('List - 0 alebo viac položiek uložených ako jeden objekt; položky možno meniť, pridávať a odstraňovať | Syntax: [x,y,z]'):
            st.code('''
            l = [1,2,3,4,2,3,4,5,6,7,8,98]
            l, type(l)
            ''')

            l = [1, 2, 3, 4, 2, 3, 4, 5, 6, 7, 8, 98]

            st.write(l, str(type(l)))
            st.subheader('Práca s listom')
            st.write('Výber prvého prvku')
            st.code('''l[0]''')
            st.write(l[0])

            st.write('Počet prvkov')
            st.code('''len(l)''')
            st.write(len(l))

            st.write('Výber posledného prvku')
            st.code('''l[-1]''')
            st.write(l[-1])

            st.write('Pridanie prvku')
            st.code('''
                l.append(10)
                l
            ''')
            l.append(10)
            st.write(l)

            st.write('Vymazanie n-tého prvku')
            st.code('''
            l.pop(2)
            l
            ''')
            l.pop(2)
            st.write(l)

            st.write('K časti listu môžeme pristupovať pomocou my_list[i:j], kde i je začiatok plátku (indexovanie opäť začína od 0) a j koniec plátku. Napríklad:')
            st.code('''l[1:1], l[0:2], l[1:-1], l[1:-2]''')
            st.write(l[1:1], l[0:2], l[1:-1], l[1:-2])

            st.write('Súčet všetkých prvkov')
            st.code('''sum(l)''')
            st.write(sum(l))

            st.write('Najväčší prvok a najmenší prvok')
            st.code('''max(l), min(l)''')
            st.write(max(l), min(l))

            st.write('Usporiadanie listu')
            st.code('''l.sort(reverse=True)''')
            l.sort(reverse=True)
            st.write(l)
            st.code('''l.sort(reverse=False)''')
            l.sort(reverse=False)
            st.write(l)

        with st.expander('Dictionary - 0 alebo viac položiek vzájomne mapovaných v štruktúre kľúč-atribút | Syntax: {kľúč:atribút}'):
            st.code('''
            d = {
                "name": "John",
                "surname": "Smith",
                "age" : 25,
                "is_married": True,
                "children": ["Alice", "Bob"],
            }
            d2 = {
                "name": "Mathew",
                "surname": "Smith",
                "age" : 20,
                "is_married": False,
                "children": [],
            }
            d, d2
            ''')
            d = {
                "name": "John",
                "surname": "Smith",
                "age": 25,
                "is_married": True,
                "children": ["Alice", "Bob"],
            }
            d2 = {
                "name": "Mathew",
                "surname": "Smith",
                "age": 20,
                "is_married": False,
                "children": [],
            }
            st.write(d, d2)
            st.write('Hodnota kľúča "name" v dictionary d')
            st.code('''d["name"]''')
            st.write(d["name"])

            st.write('Usporiadanie listu dictionaries')
            st.code('''
            list_d = [d, d2]
            list_d
            ''')
            list_d = [d, d2]
            st.write(list_d, list_d)

            st.code('''
            list_d.sort(key=lambda item: item['age'], reverse=True)
            list_d
            ''')
            list_d.sort(key=lambda item: item['age'], reverse=True)
            st.write(list_d)

        with st.expander('Set - 0 alebo viac položiek uložených ako jeden objekt, položky v sade nemožno meniť, ale možno pridávať nové položky; žiadne duplikáty'):
            st.code('''
                s = {
                    "New Orleans",
                    "Louisiana",
                    "NOLA",
                    "New Orleans"
                    }
                s
            ''')
            s = {
                "New Orleans",
                "Louisiana",
                "NOLA",
                "New Orleans"
            }
            st.write(s)
            st.write('Pridanie prvku do setu')
            st.code('''
            s.add("Texas")
            s
            ''')
            s.add("Texas")
            st.write(s)

            st.write('Duplikátny prvok sa do setu nepridá')
            st.code('''
            s.add("Texas")
            s
            ''')
            st.write(s)
            st.write('Výber zo setu')
            st.code('''list(s)[1:3]''')
            st.write(list(s)[1:3])

            st.write('Usporiadanie setu')
            st.code('''sorted(s, reverse=True)''')
            st.write(sorted(s, reverse=True))

        with st.expander('Tuple - 0 alebo viac položiek uložených ako jeden objekt, položky v tuple nemožno meniť a nemožno pridávať nové položky'):

            st.code('''
            t = (0, 12, 1, 1834)
            t, type(t)
            ''')
            t = (0, 12, 1, 1834)
            st.write(t, str(type(t)))
            st.code('''t[1]''')
            st.write(t[1])
            st.write('Usporiadanie listu tuple')
            st.code('''tuple(sorted(t))''')
            st.write(tuple(sorted(t)))

    with st.expander('Podmienky'):
        st.write('Ako naznačuje ich názov, podmienené príkazy predstavujú spôsob vykonávania kódu v závislosti od toho, či je podmienka True alebo False. Podobne ako v iných jazykoch, aj Python podporuje if a else, ale else if sa skracuje na elif, ako ukazuje príklad nižšie.')
        st.code('''
            my_variable = 5
            if my_variable < 0:
              print("negative")
            elif my_variable == 0:
              print("zero")
            else: # my_variable > 0
              print("positive")
        ''')
        st.write(print("positive"))
        st.code('''
        my_variable = 0
        if my_variable < 0:
          print("negative")
        elif my_variable == 0:
          print("zero")
        else: # my_variable > 0
          print("positive")
        ''')
        st.write(print("zero"))

        st.code('''
        my_variable = -1
        if my_variable < 0:
          print("negative")
        elif my_variable == 0:
          print("zero")
        else: # my_variable > 0
          print("positive")
        ''')
        st.write(print("negative"))

        st.write('Je prvok v liste?')
        st.code('''
        l = [0,1,2,3,4,5,6,7,8,9]
        1 in l
        ''')
        l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        st.write(1 in l)
        st.write('Nie je znak v stringu?')
        st.code('''
        s = 'string'
        "s" not in string
        ''')
        s = 'string'
        st.write("s" not in string)

        st.write('Má prvok hodnotu?')
        st.code('''string is not None''')
        st.write(string is not None)

        st.write('Su stringy rovnaké?')
        st.code('''"some text" == string''')
        st.write("some text" == string)

        st.write('< a > sú striktné operátory menšie a väčšie ako, zatiaľ čo == je operátor rovnosti (nemýliť si s =, operátorom priradenia premennej). Operátory <= a >= možno použiť na porovnávanie menšieho (resp. väčšieho) ako alebo rovnakého.')
        st.write('Na rozdiel od iných jazykov sa bloky kódu oddeľujú pomocou odsadenia. Tu používame odsadenie na 2 medzery, ale mnohí programátori používajú aj odsadenie na 4 medzery. Ktorékoľvek z nich je v poriadku, pokiaľ ste v celom kóde konzistentní.')

    with st.expander('Cykly'):
        st.write('Slučky predstavujú spôsob viacnásobného vykonania bloku kódu. Existujú dva hlavné typy cyklov: cykly while a cykly for.')
        st.write('While cyklus')
        st.code('''
            i = 0
            while i < len(l):
              print(l[i])
              i += 1
        ''')
        i = 0
        while i < len(l):
            st.write(l[i])
            i += 1
        st.write('For cyklus naprieč indexami')
        st.code('''
        for i in range(100, 0, -5):
          print(i)
        ''')
        for i in range(100, 0, -5):
            print(i)

        st.write('For cyklus naprieč prvkami')
        st.code('''
        l = [0,1,2,3,4,5,6,7,8,9]
        for item in l:
          print(item)
        ''')
        l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for item in l:
            st.write(item)

        st.write('Jednoriadkový for cyklus, pre prácu s listami')
        st.write('Pretypovanie všetkých prvkov na stringy, reťazce')
        st.code('''[str(item) for item in l]''')
        st.write([str(item) for item in l])

        st.write('Pretypovanie prvkov menšich ako 5 na stringy, reťazce')
        st.code('''[str(item) for item in l if item < 5]''')
        st.write([str(item) for item in l if item < 5])
        st.code('''[str(item) if item < 5 else "5" for item in l]''')
        st.write([str(item) if item < 5 else "5" for item in l])

    with st.expander('Funkcie'):
        st.write('Na zlepšenie čitateľnosti kódu je bežné rozdeliť kód do rôznych blokov, ktoré sú zodpovedné za vykonávanie presných činností: funkcií. Funkcia prijíma nejaké vstupy a spracúva ich, aby vrátila nejaké výstupy.')

        st.code('''
            def square(x):
                return x**2
            square(5)
        ''')

        def square(x):
            return x ** 2
        st.write(square(5))

        st.code('''
        def multiply(a, b):
            return a*b
        multiply(2, 3)
        ''')

        def multiply(a, b):
            return a * b
        st.write(multiply(2, 3))
        st.code('''square(x=multiply(a=2, b=3))''')
        st.write(square(x=multiply(a=2, b=3)))

    with st.expander('Príklad 6.1'):
        st.write('Vytvorte funkciu, ktorá pomocou for cyklu vytvorí pre každého supliera celkovú cenu, a priraďťe túto hodnotu do dictionary daného usera pod kľúčom "total_price"')
        st.code('''
            supply_bids = [
                {"supplier": "Supplier A", "price": 30, "quantity": 100},
                {"supplier": "Supplier B", "price": 35, "quantity": 150},
                {"supplier": "Supplier C", "price": 40, "quantity": 200},
                {"supplier": "Supplier D", "price": 45, "quantity": 120},
                {"supplier": "Supplier E", "price": 50, "quantity": 80}
            ]
        ''')
        supply_bids = [
            {"supplier": "Supplier A", "price": 30, "quantity": 100},
            {"supplier": "Supplier B", "price": 35, "quantity": 150},
            {"supplier": "Supplier C", "price": 40, "quantity": 200},
            {"supplier": "Supplier D", "price": 45, "quantity": 120},
            {"supplier": "Supplier E", "price": 50, "quantity": 80}
        ]

        st.code('''
        def total_cost(supply_bids):
            for supplier in supply_bids:
                supplier["total_price"] = supplier["price"] * supplier["quantity"]
            return supply_bids
            total_cost(supply_bids)
        ''')

        def total_cost(supply_bids):
            for supplier in supply_bids:
                supplier["total_price"] = supplier["price"] * supplier["quantity"]
            return supply_bids
        st.write(total_cost(supply_bids))
