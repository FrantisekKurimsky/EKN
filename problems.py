import pandas as pd

math_problems_1 = [
    {
        "question": "Banka poskytuje 11 % ročný úrok na uložených vkladoch. Banka pripisuje úroky v poslednom dni každého štvrťroka. Peniaze uložené na vklad sa úročia na bežný mesiac, ak sú vložené do 8. dňa v bežnom mesiaci. Občan si otvoril účet 8. januára a vložil 5000 €. Aký veľký úrok získa do 30. júna?",
        "solution": r"\text{základ úrokovania: } i=\frac{p}{100}, \\[5mm] p: \text{percentová úroková miera a } i: \text{úroková sadzba,} \\[5mm] \text{začiatočná hodnota kapitálu (istiny) : } K_0, \\[5mm] \text{dĺžka úrokového obdobia : } n, \\[5mm] u=K_0⋅i⋅n \\[5mm] \text{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_} \\ \text{Jan, Feb, Mar, Apr, Maj, Jun, } \\[5mm] \text{30.Jun presne druhé švtrťročie, preto berieme do úvahy polovicu roka,}\\[5mm] \text{a teda polovicu z 11\% z 5000 €} \\[5mm] u = 5000 * 0.11 * \frac{1}{2} \\[5mm] u = \frac{550}{2} \\[5mm] u = 275",
        "table": None,
        "code": None
    },
    {
        "question": "Banka poskytuje na vkladoch 8 % ročný úrok. Karol potrebuje za 9 mesiacov vrátiť dlžobu 5000 €. Koľko musí  teraz vložiť do banky, aby mal za 9 mesiacov k dispozícii práve túto sumu?",
        "solution": r"K_0 + u = 5000 \\[5mm] K_0 + K_0 * i * n = 5000 \\[5mm] K_0 + K_0 + 0.08 * 9/12 = 5000 \\[5mm] K_0 * (1 + 0.08 * 9/12) = 5000 \\[5mm] K_0 * (1 + 0.08 * 3/4) = 5000 \\[5mm] K_0 * 1.06 = 5000 \\[5mm] K_0 = 5000 / 1.06",
        "table": None,
        "code": '5000 / 1.06'
    },
    {
        "question": "Helena investovala 5000 € na zamestnanecký účet, ktorý prináša 8 % ročný úrok. Ako dlho má ponechať túto sumu na účte, aby získala 300€?",
        "solution": r"u = K_0 * i * n \\[5mm] 300 = K_0 * i * n \\[5mm] 300 = 5000 * 0.08 * n \\[5mm] n = \frac{300}{5000*0.08} \\[5mm] n = \frac{300}{400} = 3/4 \text{ roka} = 9 \text{ mesiacov}",
        "table": None,
        "code": None
    },
    {
        "question": "Inštalovaný výkon modelovej elektrizačnej sústavy je koncom roka 2023  P_i = 234 GW. Aký veľký inštalovaný výkon bude mať táto sústava roku 2029, ak predpokladáme každoročný vzrast inštalovaného výkonu o 6%?",
        "solution": r"\text{Zložené úrokovanie} \\[5mm] \text{Kapitál na začiatku 1. periódy |} K_0 \\[5mm] \text{Kapitál na konci 1. periódy | } K_1 = K_0 + u = K_0 + K_0 * i = K_0 (1 + i) \\[5mm] \text{Kapitál na konci 2. periódy | } K_2  = K_1 + K_1 * i = K_1 (1 + i) = K_0 * (1 + i) (1 + i) \\[5mm] \text{Kapitál na konci n-tej periódy| } K_n = K_0 * (1 + i)^ n \\[1cm] K_n \text{ sa nazýva budúca hodnota, }\\ K_0 \text{ je súčasná hodnota, } \\ \text{kde } r^n = (1+i)^n \\ \text{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_} \\ P_{i 2029} = P_{i 2023} * (1 + i) ^ n \\[5mm] n = 6 rokov, \\[5mm] P_{i 2029} = 234 * 1.06^6 GW",
        "table": None,
        "code": "234 * 1.06 ** 6"
    },
    {
        "question": "Na účely budúcej investičnej výstavby začiatkom roku 2030 ukladá podnik do banky podľa dlhodobého finančného plánu na konci uvedených rokov čiastky podľa nasledujúcej tabuľky. Akú  čiastku bude mať podnik k dispozícii pri začatí výstavby, ak úroková miera p=6%?",
        "table": pd.DataFrame({
            "Rok": [int(x) for x in [2020, 2021, 2022, 2024, 2026, 2028]],
            "K (mil. Eur)": [3.8, 4.1, 3.6, 3.9, 4.0, 3.7]
        }).T,
        "solution": r"\text{Začiatkom roka 2030 potrebujeme peniaze, teda postupne} \\[5mm] K_{2020-2029} = 3.8 * (1 + 0.06) ^ 9 \\[5mm] K_{2021-2029} = 4.1 * (1 + 0.06) ^ 8 \\ \vdots \\ K_{2028-2029} = 3.7 * (1 + 0.06) ^ 1 \text{Spolu: } \\[5mm] K_{2030} = 3.8 * 1.06^9 + 4.1 * 1.06^8 + 3.6 * 1.06^7 + 3.9 * 1.06^5 + 4 * 1.06^3 + 3.7*1.06 = ",
        "code": "3.8 * 1.06**9 + 4.1 * 1.06**8 + 3.6 * 1.06**7 + 3.9 * 1.06**5 + 4 * 1.06**3 + 3.7*1.06"

    },
    {
        "question": "Rozhodnite, o aký investičný úver má dnes požiadať podnik banku, aby pri úrokovej miere p = 6% mohol tento úver práve splatiť po 9 rokoch predpokladanými voľnými finančnými zdrojmi (odpismi a časťou zisku), ktoré sa budú podľa dlhodobého plánu podniku tvoriť tak, ako je vidieť z nasledujúcej tabuľky:",
        "solution": r"\textbf{Zložené odúrokovanie (diskontovanie)} \\[3mm] \text{Výpočet súčasnej hodnoty  kapitálu } K_0 \text{ v závislosti od budúcej hodnoty } K_n. \\[3mm] \text{diskont } D = K_n - K_0. \\[3mm] \text{Prepočet budúcej hodnoty na súčasnú : } \\ K_0 = K_n*(1+i)^{-n}, \\[3mm] \text{zložený odúročiteľ je: }\\ r^{-n} = (1+i)^{-n} \\ \text{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_} \\[5mm] K_0 = 13 * 1.06^{-1} + 15 * 1.06^{-2} + 16*1.06^{-4} + 17 * 1.06^{-6} + 16 * 1.06^{-8} + 17*1.06^{-9} = " ,
        "table": pd.DataFrame({
            "Rok": [int(x) for x in [1, 2, 4, 6, 8, 9]],
            "K (mil. Eur)": [13, 15, 16, 17, 18, 17]
        }).T,
        "code": "(13 * (1.06**(-1))) + (15 * (1.06**(-2))) + (16 * (1.06**(-4))) + (17 * (1.06**(-6))) + (16 * (1.06**(-8))) + (17 * (1.06**(-9)))"

    },
    {
        "question": "Aká bude celková hodnota uloženého radu každoročných konštantných platieb vo výške K = 2500 € po 20 rokov pri p = 2 %?",
        "solution": r"\textbf{Sporiteľ } \text{určuje budúcu hodnotu } n \text{ pravidelných platieb koncom období.} \\[3mm] \text{Vypočíta sa ako súčet } n \text{ členov geometrickej postupnosti.} \\[3mm]s_n = \sum_{t=1}^{n}{r^{n-t}} = r^{n-1} + r^{n-2} + r^{n-3} + \dots +r^{n-n} \\[3mm] s_n = \frac{r^n - 1}{r-1}. \\[3mm] r^n = (1+i)^n \\[5mm] K_{20} = \frac{r^n - 1 }{r - 1} * K\\[3mm] K_{20} = \frac{1.02^{20} -1 }{1.02 - 1} * 2500\\[3mm] K_{20} = \frac{1.02^{20} -1 }{0.02} *2500 \\[3mm]K_{20} = \frac{0.4859473}{0.02} * 2500 = 24.297365 * 2500 = 60743.4125" ,
        "table": None,
        "code": "((1.02**20 -1)/0.02) *2500"

    },
    {
        "question": "Aká je súčasná celková hodnota uloženého radu konštantných platieb z príkladu 1.7?",
        "solution": r"\textbf{Zásobovateľ } \text{určuje súčasnú hodnotu n jednotkových}\\[3mm] \text{pravidelných platieb koncom období.} \\[3mm] \text{Vypočíta sa ako súčet n členov geometrickej postupnosti.} \\[3mm] z_n = \sum_{t=1}^{n}{r^{-t}} = r^{-1} + r^{-2} + r^{-3} + \dots + r^{-n} \\[3mm] z_n = \frac{r^n-1}{r^n*(r-1)}\\[5mm] K_0 = \frac{r^{20} - 1}{r^{20} * (r-1)} * K \\[3mm] K_0 = \frac{1.02^{20}-1}{1.02^{20}*(1.02-1)}*2500\\[3mm]K_0 = \frac{1.02^{20}-1}{1.02^{20}*0.02}*2500\\[5mm] \text{Teda ak chceme naraz zaplatiť sumu tak,}\\[2mm] \text{aby sme po 20 rokoch získali 60743.4245,} \\[2mm] \text{potrebujeme zaplatiť 40878.5834.}\\[2mm] \text{Pravidelnými platbami zaplatíme } 2500*20=5000 € \\[5mm] \text{Príklad môžeme riešiť jednoduchšie, diskontovaním na začiatku obdobia} \\[3mm] K_0 = K_{20} * r^{-20} \\[3mm] K_0 = 60743.4245 * 1.02^{-20} = 40878.5834" ,
        "table": None,
        "code": "((1.02**20-1)/(1.02**20*0.02))*2500"

    },
    {
        "question": "Akú čiastku musí občan ukladať, aby o 6 rokov mal na účte potrebnú sumu v hodnote 352000 € pri úrokovej miere 4 % ?",
        "solution": r"AHOJ \textbf{Fondovateľ } \text{vyjadruje stanovenie radu každoročných konštantných platieb, }\\[3mm]\text{ktoré v budúcnosti vytvoria požadovanú hodnotu. }\\[3mm]\text{Jeho výpočet je prevrátenou hodnotou sporiteľa:} \\[3mm] f_n = \frac{r-1}{r^n-1}\\[5mm] K = \frac{r-1}{r^6-1}*K_6\\[3mm]K = \frac{1.04-1}{1.04^6-1}*352000" ,
        "table": None,
        "code": "((1.04-1)/(1.04**6-1))*352000"

    },
]