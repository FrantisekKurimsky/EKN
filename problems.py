import pandas as pd

math_problems_1 = [
    {
        "question": "Banka poskytuje 11 % ročný úrok na uložených vkladoch. Banka pripisuje úroky v poslednom dni každého štvrťroka. Peniaze uložené na vklad sa úročia na bežný mesiac, ak sú vložené do 8. dňa v bežnom mesiaci. Občan si otvoril účet 8. januára a vložil 5000 €. Aký veľký úrok získa do 30. júna?",
        "solution": r"\text{základ úrokovania: } i=\frac{p}{100}, \\[5mm] p: \text{percentová úroková miera a } i: \text{úroková sadzba,} \\[5mm] \text{začiatočná hodnota kapitálu (istiny) : } K_0, \\[5mm] \text{dĺžka úrokového obdobia : } n, \\[5mm] u=K_0⋅i⋅n \\[5mm] \text{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_} \\ \text{Jan, Feb, Mar, Apr, Maj, Jun, } \\[5mm] \text{30.Jun presne druhé švtrťročie, preto berieme do úvahy polovicu roka,}\\[5mm] \text{a teda polovicu z 11\% z 5000 €} \\[5mm] u = 5000 * 0.11 * \frac{1}{2} \\[5mm] u = \frac{550}{2} \\[5mm] u = 275",
        "table": None,
        "code": None,
        "solutiontable": None
    },
    {
        "question": "Banka poskytuje na vkladoch 8 % ročný úrok. Karol potrebuje za 9 mesiacov vrátiť dlžobu 5000 €. Koľko musí  teraz vložiť do banky, aby mal za 9 mesiacov k dispozícii práve túto sumu?",
        "solution": r"K_0 + u = 5000 \\[5mm] K_0 + K_0 * i * n = 5000 \\[5mm] K_0 + K_0 + 0.08 * 9/12 = 5000 \\[5mm] K_0 * (1 + 0.08 * 9/12) = 5000 \\[5mm] K_0 * (1 + 0.08 * 3/4) = 5000 \\[5mm] K_0 * 1.06 = 5000 \\[5mm] K_0 = 5000 / 1.06",
        "table": None,
        "code": '5000 / 1.06',
        "solutiontable": None
    },
    {
        "question": "Helena investovala 5000 € na zamestnanecký účet, ktorý prináša 8 % ročný úrok. Ako dlho má ponechať túto sumu na účte, aby získala 300€?",
        "solution": r"u = K_0 * i * n \\[5mm] 300 = K_0 * i * n \\[5mm] 300 = 5000 * 0.08 * n \\[5mm] n = \frac{300}{5000*0.08} \\[5mm] n = \frac{300}{400} = 3/4 \text{ roka} = 9 \text{ mesiacov}",
        "table": None,
        "code": None,
        "solutiontable": None
    },
    {
        "question": "Inštalovaný výkon modelovej elektrizačnej sústavy je koncom roka 2023  P_i = 234 GW. Aký veľký inštalovaný výkon bude mať táto sústava roku 2029, ak predpokladáme každoročný vzrast inštalovaného výkonu o 6%?",
        "solution": r"\text{Zložené úrokovanie} \\[5mm] \text{Kapitál na začiatku 1. periódy |} K_0 \\[5mm] \text{Kapitál na konci 1. periódy | } K_1 = K_0 + u = K_0 + K_0 * i = K_0 (1 + i) \\[5mm] \text{Kapitál na konci 2. periódy | } K_2  = K_1 + K_1 * i = K_1 (1 + i) = K_0 * (1 + i) (1 + i) \\[5mm] \text{Kapitál na konci n-tej periódy| } K_n = K_0 * (1 + i)^ n \\[1cm] K_n \text{ sa nazýva budúca hodnota, }\\ K_0 \text{ je súčasná hodnota, } \\ \text{kde } r^n = (1+i)^n \\ \text{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_} \\ P_{i 2029} = P_{i 2023} * (1 + i) ^ n \\[5mm] n = 6 rokov, \\[5mm] P_{i 2029} = 234 * 1.06^6 GW",
        "table": None,
        "code": "234 * 1.06 ** 6",
        "solutiontable": None
    },
    {
        "question": "Na účely budúcej investičnej výstavby začiatkom roku 2030 ukladá podnik do banky podľa dlhodobého finančného plánu na konci uvedených rokov čiastky podľa nasledujúcej tabuľky. Akú  čiastku bude mať podnik k dispozícii pri začatí výstavby, ak úroková miera p=6%?",
        "table": pd.DataFrame({
            "Rok": [int(x) for x in [2020, 2021, 2022, 2024, 2026, 2028]],
            "K (mil. Eur)": [3.8, 4.1, 3.6, 3.9, 4.0, 3.7]
        }).T,
        "solution": r"\text{Začiatkom roka 2030 potrebujeme peniaze, teda postupne} \\[5mm] K_{2020-2029} = 3.8 * (1 + 0.06) ^ 9 \\[5mm] K_{2021-2029} = 4.1 * (1 + 0.06) ^ 8 \\ \vdots \\ K_{2028-2029} = 3.7 * (1 + 0.06) ^ 1 \text{Spolu: } \\[5mm] K_{2030} = 3.8 * 1.06^9 + 4.1 * 1.06^8 + 3.6 * 1.06^7 + 3.9 * 1.06^5 + 4 * 1.06^3 + 3.7*1.06 = ",
        "code": "(3.8 * 1.06**9) + (4.1 * 1.06**8) + (3.6 * 1.06**7) + (3.9 * 1.06**5) + (4 * 1.06**3) + (3.7*1.06)",
        "solutiontable": None

    },
    {
        "question": "Rozhodnite, o aký investičný úver má dnes požiadať podnik banku, aby pri úrokovej miere p = 6% mohol tento úver práve splatiť po 9 rokoch predpokladanými voľnými finančnými zdrojmi (odpismi a časťou zisku), ktoré sa budú podľa dlhodobého plánu podniku tvoriť tak, ako je vidieť z nasledujúcej tabuľky:",
        "solution": r"\textbf{Zložené odúrokovanie (diskontovanie)} \\[3mm] \text{Výpočet súčasnej hodnoty  kapitálu } K_0 \text{ v závislosti od budúcej hodnoty } K_n. \\[3mm] \text{diskont } D = K_n - K_0. \\[3mm] \text{Prepočet budúcej hodnoty na súčasnú : } \\ K_0 = K_n*(1+i)^{-n}, \\[3mm] \text{zložený odúročiteľ je: }\\ r^{-n} = (1+i)^{-n} \\ \text{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_} \\[5mm] K_0 = 13 * 1.06^{-1} + 15 * 1.06^{-2} + 16*1.06^{-4} + 17 * 1.06^{-6} + 16 * 1.06^{-8} + 17*1.06^{-9} = " ,
        "table": pd.DataFrame({
            "Rok": [int(x) for x in [1, 2, 4, 6, 8, 9]],
            "K (mil. Eur)": [13, 15, 16, 17, 18, 17]
        }).T,
        "code": "(13 * (1.06**(-1))) + (15 * (1.06**(-2))) + (16 * (1.06**(-4))) + (17 * (1.06**(-6))) + (16 * (1.06**(-8))) + (17 * (1.06**(-9)))",
        "solutiontable": None

    },
    {
        "question": "Aká bude celková hodnota uloženého radu každoročných konštantných platieb vo výške K = 2500 € po 20 rokov pri p = 2 %?",
        "solution": r"\textbf{Sporiteľ } \text{určuje budúcu hodnotu } n \text{ pravidelných platieb koncom období.} \\[3mm] \text{Vypočíta sa ako súčet } n \text{ členov geometrickej postupnosti.} \\[3mm]s_n = \sum_{t=1}^{n}{r^{n-t}} = r^{n-1} + r^{n-2} + r^{n-3} + \dots +r^{n-n} \\[3mm] s_n = \frac{r^n - 1}{r-1}. \\[3mm] r^n = (1+i)^n \\[5mm] K_{20} = \frac{r^n - 1 }{r - 1} * K\\[3mm] K_{20} = \frac{1.02^{20} -1 }{1.02 - 1} * 2500\\[3mm] K_{20} = \frac{1.02^{20} -1 }{0.02} *2500 \\[3mm]K_{20} = \frac{0.4859473}{0.02} * 2500 = 24.297365 * 2500 = 60743.4125" ,
        "table": None,
        "code": "((1.02**20 -1)/0.02) *2500",
        "solutiontable": None

    },
    {
        "question": "Aká je súčasná celková hodnota uloženého radu konštantných platieb z príkladu 1.7?",
        "solution": r"\textbf{Zásobovateľ } \text{určuje súčasnú hodnotu n jednotkových}\\[3mm] \text{pravidelných platieb koncom období.} \\[3mm] \text{Vypočíta sa ako súčet n členov geometrickej postupnosti.} \\[3mm] z_n = \sum_{t=1}^{n}{r^{-t}} = r^{-1} + r^{-2} + r^{-3} + \dots + r^{-n} \\[3mm] z_n = \frac{r^n-1}{r^n*(r-1)}\\[5mm] K_0 = \frac{r^{20} - 1}{r^{20} * (r-1)} * K \\[3mm] K_0 = \frac{1.02^{20}-1}{1.02^{20}*(1.02-1)}*2500\\[3mm]K_0 = \frac{1.02^{20}-1}{1.02^{20}*0.02}*2500\\[5mm] \text{Teda ak chceme naraz zaplatiť sumu tak,}\\[2mm] \text{aby sme po 20 rokoch získali 60743.4245,} \\[2mm] \text{potrebujeme zaplatiť 40878.5834.}\\[2mm] \text{Pravidelnými platbami zaplatíme } 2500*20=50000 € \\[5mm] \text{Príklad môžeme riešiť jednoduchšie, diskontovaním na začiatku obdobia} \\[3mm] K_0 = K_{20} * r^{-20} \\[3mm] K_0 = 60743.4245 * 1.02^{-20} = 40878.5834" ,
        "table": None,
        "code": "((1.02**20-1)/(1.02**20*0.02))*2500",
        "solutiontable": None

    },
    {
        "question": "Akú čiastku musí občan ukladať, aby o 6 rokov mal na účte potrebnú sumu v hodnote 352000 € pri úrokovej miere 4 % ?",
        "solution": r"\textbf{Fondovateľ } \text{vyjadruje stanovenie radu každoročných konštantných platieb, }\\[3mm]\text{ktoré v budúcnosti vytvoria požadovanú hodnotu. }\\[3mm]\text{Jeho výpočet je prevrátenou hodnotou sporiteľa:} \\[3mm] f_n = \frac{r-1}{r^n-1}\\[5mm] K = \frac{r-1}{r^6-1}*K_6\\[3mm]K = \frac{1.04-1}{1.04^6-1}*352000" ,
        "table": None,
        "code": "((1.04-1)/(1.04**6-1))*352000",
        "solutiontable": None

    },
    {
        "question": "Podnik žiada od banky úver na realizáciu investičných zámerov vo výške 2,3 mil. €. Banka poskytla úver zo splatnosťou 10 rokov pri  p = 6 %. Akou čiastkou spláca podnik každoročne dlžobu?",
        "solution": r"\textbf{Umorovateľ} \text{ vyjadruje splácanie (umorovanie) pôžičky, resp. výpočet budúcich hodnôt} \\[3mm] \text{každoročných konštantných platieb zo súčasnej hodnoty pôžičky.} \\[3mm] \text{Určuje opakované splátky koncom n období zo súčasnej jednotkovej hodnoty (anuita zo súčasnej hodnoty} \\[3mm]\text{). Jeho výpočet je prevrátenou hodnotou zásobovateľa:} \\[3mm]a_n = \frac{r^n*(r-1)}{r^n-1} \\[6mm] A = \frac{r^{10}*(r-1)}{r^{10}-1}*K_0 \\[4mm] A = \frac{1.06^{10}*0.06}{1.06^{10}-1} * 2.3 * 10^6" ,
        "table": None,
        "code": "(((1.06**10)*0.06)/((1.06**10) - 1)) * 2.3 * 10**6",
        "solutiontable": None

    },
    {
        "question": "Podnik má splatiť pôžičku 100000 € za 5 rokov pri úrokovej sadzbe 3,5 %. Vyhotovte umorovací plán platenia dlžoby! Výpočet realizujte a)	pre konštantnú anuitu, b)   pre konštantný úmor.",
        "solution": None,
        "table": None,
        "solutiontable": {
            "a": pd.DataFrame({
                "Úroková perióda": ["0", "1", "2", "3", "4", "5", "celkom"],
                "Zvyšok dlžoby [€]": ["100000", "81350.00", "62047.25", "42068.91", "21391.32", "0.00", ""],
                "Úroky [€]": ["-", "3500.00", "2847.25", "2171.66", "1472.41", "748.70", "10740.02"],
                "Úmor [€]": ["-", "18650.00", "19302.75", "19978.34", "20677.59", "21391.32", "100000"],
                "Splatené [€]": ["0", "18650.00", "37952.75", "57931.09", "78608.68", "100000.00", ""],
                "Splatka": ["", "22150.00", "22150.00", "22150.00", "22150.00", "22140.02", ""]
            }),
            "b": pd.DataFrame({
                    "Úroková perióda": ["0", "1", "2", "3", "4", "5", "celkom"],
                    "Zvyšok dlžoby [€]": ["100000", "80000", "60000", "40000", "20000", "0", ""],
                    "Úroky [€]": ["-", "3500", "2800", "2100", "1400", "700", "10500"],
                    "Úmor [€]": ["-", "20000", "20000", "20000", "20000", "20000", "100000"],
                    "Splatené [€]": ["0", "20000", "40000", "60000", "80000", "100000", ""],
                    "Splátka[€]": ["-", "23500", "22800", "22100", "21400", "20700", ""]
            }),
        },
        "code": None

    },
]

math_problems_2 = [
    {
        "question": "Ak sú tržby v 7. roku prevádzky  V7  = 100 mil. € a  q = 1,05, vtedy aktualizovaná hodnota uvedených tržieb k začiatku prvého roku prevádzky je ...",
        "solution": r"z = \frac{\Delta{D_s}}{\Delta{P_s}} \\[3mm] z: \text{inkrementálny činiteľ času} \\[3mm] \Delta{D_s}: \text{prírastok  dôchodku za zvolený časový interval} \\[3mm] \Delta{P_s}: \text{prírastok vynaložených materiálnych prostriedkov na dosiahnutie prírastku dôchodku} \\[5mm] \text{Urýchlenie tržieb V o jeden rok predstavuje vzrast tejto tržby za tento rok na :} \\[3mm] V' = v(1+z) \\[3mm]\text{o dva roky : } V'' = V(1+z)^2 \\[3mm] \text{o n rokov : }  V''' = V(1+z)^n \\[5mm] \text{Urýchlenie tržieb V z k-teho na j-ty rok teda znamená, že táto tržba má v k-tom roku hodnotu: } V_{kj} = v_j (1+z)^{k-j} \\[3mm] V_{kj} \text{ je tržba j-teho roku prepočítaná na k-ty rok} \\[3mm] V_j \text{ je tržba v j-tom roku.} \\[5mm] \text{Podobne ako v  bankovníctve, kde výraz r = 1 + i  sa označuje názvom úročiteľ, možno zaviesť pre ďalší výklad symbol: } \\[3mm] q = 1+z. \\ \text{\_\_\_\_} \\[5mm] V_p = 10^8 * 1.05^{0-7} = ",
        "table": None,
        "code": "(10**8) * (1.05 ** (-7))",
        "solutiontable": None
    },
    {
        "question": "Ak boli investičné náklady v prvom roku výstavby Ni1 = 50 mil. € a  q = 1,05, ich aktualizovaná hodnota k začiatku prvého roku prevádzky pri čase výstavby Tv = 5 rokov je",
        "solution": r"\text{Podobne možno použiť metódu zloženého úrokovania pre prepočty nákladov a ziskov podľa :} \\[3mm] N_{kj} = N_jq^{k-j} \\[3mm] N_{kj} \text{ sú náklady j-teho roku prepočítané na k-ty rok, } \\[3mm] N_j \text{ sú náklady j-teho roku} \\[3mm]N_{ip}=N_{it}q^{T_v-T_{\Delta}-t} \\ \text{\_\_\_} \\[5mm] q^{T_v-T_{\Delta}-t} = (1+z)^{5-0-1} \\[3mm] N_{ip} = N_{i1} * 1.05^{5-1} = 50 * 10^6 * 1.05^{5-1} = ",
        "table": None,
        "code": "(50 * (10**6)) * (1.05**4)",
        "solutiontable": None
    },
    {
        "question": "Čas výstavby presahuje o 2 roky rok uvedenia do prevádzky. Výslednú aktualizovanú hodnotu nákladov z predošlého príkladu vyjadruje vzťah",
        "solution": r"\text{Ak čas výstavby presahuje termín uvedenia do prevádzky o } T_{\Delta} \text{ rokov, činiteľ má tvar  } q^{T_v-T_{\Delta}-t}, \\[5mm] N_{ip}=N_{it}q^{T_v-T_{\Delta}-t} \\[3mm] N_{ip} = 50 * 10^6 * 1.05 ^{5-2-1} = ",
        "table": None,
        "code": "(50 * (10**6)) * (1.05**2)",
        "solutiontable": None
    },
    {
        "question": "Stanovte aktualizované (prepočítané) investičné náklady, ak podľa súhrnného rozpočtu investičné náklady pre sledovanú stavbu elektrickej stanice  boli vo výške 5 mil. €. Počas  výstavby  Tv = 5 rokov boli investičné náklady čerpané takto (v percentách podľa jednotlivých rokov výstavby): 10, 15, 25, 40, 10 %. Výstavba bola skončená rok po uvedení stanice do prevádzky. Činiteľ času q = 1,05.",
        "solution": r"\text{Celkové investičné náklady sú 5 mil. €, ktoré sú rozdelené podľa nasledujúcich percent: } \\[3mm] \text{rok 1: 10 \% = 0.10×5 mil. €} \\[3mm] \text{rok 2: 15\% = 0.15×5 mil. €} \\[3mm] \text{rok 3: 25\% = 0.25×5 mil. €} \\[3mm] \text{rok 4: 40\% = 0.40×5 mil. €} \\[3mm] \text{rok 5: 10 \% = 0.10×5 mil. €} \\[5mm] \textbf{Prepočítané (aktualizované) investičné náklady }\\[3mm] N_{ip} = \sum_{t=1}^{T_v}{N_{it} q^{T_v - T_{\Delta}-t}} \\[3mm] N_{ip} = \sum_{t=1}^{5}{N_{it}} * q^{5 - 1 - t} \\[3mm] N_{ip} = 5*0.1*1.05^{5-1-1} + 5*0.15*1.05^{5-2-1} + 5*0.25*1.05^{5-3-1} + 5*0.4*1.05^{5-4-1} + 5*0.1*1.05^{5-5-1}\\[3mm] N_{ip} = 5* (0.1*1.05^{3} + 0.15*1.05^{2} + 0.25*1.05^{1} + 0.4*1.05^{0} + 0.1*1.05^{-1}) \\[3mm] N_{ip} = ",
        "table": None,
        "code": "5* (0.1*1.05**3 + 0.15*1.05**2 + 0.25*1.05**1 + 0.4*1.05**0 + 0.1*1.05**-1)",
        "solutiontable": None
    },
    {
        "question": "Stanovte ročnú kvótu pre variant výstavby elektrárne s výkonom 2 x 500 MW, ak ročné úroky sú 5% , ekonomická životnosť elektrárne je 25 rokov, pomerné náklady na údržbu  p_ú  =  0,04 / rok, pomerné náklady na mzdy  p_mz  =  0,008 / rok a ostatné pomerné náklady post  = 0.002 / rok.",
        "solution": r"\textbf{Pomerné stále náklady, tzv. ročná kvóta} \\[3mm] \text{Vyjadruje prepočet stálych nákladov (investičných a prevádzkových) na jeden priemerný rok životnosti investície} \\[3mm] k = \frac{r^{T_ž} * (r-1)}{r^{T_ž}-1} + p_ú + p_{mz} + p_{ost}\text{, kde: } \\[3mm]  p_ú \text{ : pomerné náklady na údržbu,} \\[3mm]p_{mz} \text{ : pomerné náklady na mzdy,} \\[3mm] p_{ost} \text{ : ostatné stále prevádzkové náklady (dodávky, služby, réžia atď.),} \\[3mm] T_ž \text{ :  ekonomická životnosť DHM, takisto } \\[3mm] \text{pomerná anuita (umorovateľ) } a_{T_ž} = \frac{r^{T_ž} * (r-1)}{r^{T_ž}-1} \\[3mm] \text{a pomerné stále prevádzkové náklady }k'=p_ú + p_{mz} + p_{ost}. \\ \text{\_\_\_} \\[3mm] k = \frac{1.05^{25} * (1-1.05)}{1.05^{25}-1} + 0.04 + 0.008 + 0.002 \text{ / rok}",
        "table": None,
        "code": "(((1.05**25) * (0.05)) / ((1.05**25)-1)) + 0.04 + 0.008 + 0.002",
        "solutiontable": None
    },
    {
        "question": "Vypočítajte náklady na výrobu elektrickej energie v elektrárni, ak merné investičné náklady na jej výstavbu N_i = 4300 €.kW-1, inštalovaný výkon P_i = 700 MW, čas využitia  tau=6000 h/rok, merné pohyblivé náklady n_p = 0,13 €.kW/h, kvóta k= 0,15 /rok.",
        "solution": r"N_{vr} = N_{st} + N_{po} = P_m * n_{st} + A*n_{po} = P_m *(n_{st} + \tau n_{po}) \text{ , kde: } \\[3mm] N_{vr} \text{ - ročné výrobné náklady dodávky energie,} \\[3mm] N_{st} \text{ - stála zložka ročných výrobných nákladov, }\\[3mm] N_{po} \text{ - pohyblivá zložka ročných výrobných nákladov, }\\[3mm] P_m \text{ - maximálny ročný výkon (zaťaženie) MW, }\\[3mm] A \text{ - množstvo vyrobenej energie (MWh), }\\[3mm] n_{st} \text{ - stála zložka pomerných nákladov €.MW}^{-1}.\text{rok}^{-1}, k^1 * N_i\\[3mm] n_{po} \text{ - pohyblivá zložka pomerných nákladov €.MWh}^{-1}.\text{rok}^{-1} \\[3mm] \tau \text{ - ročné využitie maximálneho výkonu.}\\[5mm] N_{vr} = 700 *10^3 * (0.15 * 4300 + 0.13 * 6000) = ",
        "table": None,
        "code": "700 *10**3  * (0.15 * 4300 + 0.13 * 6000)",
        "solutiontable": None
    },
    {
        "question": "Stanovte merné náklady na výrobu elektriny v elektrárni z predošlého príkladu.",
        "solution": r"n_v = \frac{N_v}{A} = \frac{N_v}{P_i * \tau} \\[3mm] n_v = \frac{997.5 * 10^6}{700*10^3*6000} €kWh^{-1} \\[3mm] n_v = ",
        "table": None,
        "code": "(997.5 * (10**6)) / (700*(10**3)*6000)",
        "solutiontable": None
    },
    {
        "question": "Porovnajte merné náklady na výrobu elektriny v parnej elektrárni pri časoch využitia inštalovaného výkonu  tau_1  =  6000 h.rok^-1  a tau_2  =  4000 h.rok^-1, ak merné investičné náklady elektrárne N_i  =  5100  €.kW^-1, ekonomická životnosť T_ž  =  30 rokov, merná spotreba tepla     Q_t  =  11,2 MJ.kWh^-1,  cena paliva c_pal  =  12 €.GJ^-1, ostatné stále a pohyblivé náklady odhadneme prirážkou 10% z nákladov na investície a palivo; ročné úroky sú 5%, pomerné náklady na opravu a údržbu 4%.",
        "solution": r"\text{Náklady na palivo : } \\[3mm] n_{pal} = Q_t * c_{pal} = 11.2 * 10^{-3} * 12 = 0.1344 €*kWh^{-1} \\[3mm] \text{ročná kvóta : }\\[3mm] k = \frac{1}{T_ž} + p_a + p_ú + p_{mz} + p_{ost},    p_a \thickapprox 0.03 \\[3mm] k = \frac{1}{30} + 0.03 + 0.04 = 0.103 \\[3mm] \text{merné náklady : } \\[3mm] n_v =(\frac{n_{st}}{\tau} + n_{pal}) * (1 + 0.1) \\[3mm] n_v = (\frac{k*N_i}{\tau} + n_{pal}) * 1.1 \\[3mm] n_v = (\frac{0.103 * 5100}{\tau} + 0.1344) *1.1 \\[3mm] n_{v1} = (\frac{525.3}{6000} + 0.1344) * 1.1  = 0.244145 €.kWh^{-1} \\[3mm] n_{v2} = (\frac{525.3}{4000} + 0.1344) * 1.1 = 0.2922975 €.kWh^{-1} \\[3mm] n_{v1} < n_{v2}",
        "table": None,
        "code": None,
        "solutiontable": None
    },
    {
        "question": "Očakávané ročné cash flow sú 25 000 tis. € počas štyroch rokov. Nech je miera inflácie  6 % a cena kapitálu na finančnom trhu  (úroková miera pre diskontovanie) 15 %. Aká je súčasná hodnota cash flow (SH CF) po zohľadnení inflácie?",
        "solution": r"text{a) Riešenie cez nominálnu sadzbu: } \\[3mm] \text{Najprv zohľadníme 6\% infláciu úročením očakávaných cash flow (CF)} \\[3mm] \text{a potom jednotlivé CF diskontujeme, aby sme získali ich súčasnú hodnotu.} \\[5mm] \text{b) Prepočet cez reálnu úrokovú mieru:} \\[3mm] i_r = \frac{i-m}{1+m} = \frac{0.15-0.06}{1+0.06} = 0.085 \\[3mm] \text{Reálna úroková sadzba je 8,5 \%.} \\[5mm] \text{výpočet SHCF pomocou zásobiteľa : } \\[3mm] z_4 = \frac{(1+0.085)^4 - 1}{(1 + 0.085)^4 * 0.085} = 3.2756 \\[3mm] \text{Súčasná hodnota CF pre 8,5 \%  je: } \\[3mm] 25000 * z_4 = 25000 * 3.2756 = 81890 \text{tis. €}",
        "table": None,
        "code": None,
        "solutiontable": {
            "a": pd.DataFrame({
                "rok": ["", "1.", "2.", "3.", "4.", "spolu"],
                "cash flow": ["(očakávané)", "25000", "25000", "25000", "25000", "100000"],
                "inflácia": ["(úročenie)", "(1+0,06)1", "(1+0,06)2", "(1+0,06)3", "(1+0,06)4", "-"],
                "cash flow": ["(s infláciou)", "26 500", "28 090", "29 775", "31 562", "115 927"],
                "disk.sadzba": ["15 %", "0,8696", "0,7561", "0,6575", "0,5718", "-"],
                "SHCF": ["", "23 044", "21 239", "19 577", "18 047", "81 908"]
            })
        }
    },
]