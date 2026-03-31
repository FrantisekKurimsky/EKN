import streamlit as st
import pandas as pd
from pathlib import Path
import os

# ── helper ────────────────────────────────────────────────────────────────────
def img(path: str, caption: str = ""):
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"📷 Obrázok nenájdený: `{path}`")

def code_block(code: str):
    st.code(code, language="python")

# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────

def predict_page():
    st.title("Predikcia výroby elektrickej energie z vetra")
    st.markdown(
        """
        Táto stránka prezentuje celý postup — od načítania meteorologických dát až po porovnanie
        štyroch neurónových sietí pri predikcii **hodinovej výroby vetra** (v GW).
        """
    )
    st.divider()
    
    st.header("📁 Dátové súbory (ERA5 NetCDF)")
    st.markdown(
        """
        Nižšie sú k dispozícii všetky meteorologické NetCDF súbory z priečinka
        `docs/data-weather-nc`. Každý súbor obsahuje hodinové ERA5 dáta
        (u100, v100, t2m, sp, d2m, tcc) pre danú krajinu za rok 2025.
        """
    )
    
    DATA_DIR = Path("docs/data-weather-nc")
    
    if not DATA_DIR.exists():
        st.warning(
            f"⚠️ Priečinok `{DATA_DIR}` nebol nájdený. "
            "Uistite sa, že existuje relatívne k miestu spustenia aplikácie."
        )
    else:
        files = sorted(DATA_DIR.iterdir())
        nc_files = [f for f in files if f.is_file()]
    
        if not nc_files:
            st.info("Priečinok je prázdny.")
        else:
            # Group into rows of 4 columns
            COLS = 4
            rows = [nc_files[i : i + COLS] for i in range(0, len(nc_files), COLS)]
    
            for row in rows:
                cols = st.columns(COLS)
                for col, fpath in zip(cols, row):
                    size_mb = fpath.stat().st_size / (1024 * 1024)
                    label = fpath.stem                      # filename without extension
                    ext   = fpath.suffix.lstrip(".")        # e.g. "nc"
    
                    with col:
                        with open(fpath, "rb") as fh:
                            data = fh.read()
                        st.download_button(
                            label=f"⬇️ {label}",
                            data=data,
                            file_name=fpath.name,
                            mime="application/octet-stream",
                            help=f"{fpath.name}  •  {size_mb:.1f} MB",
                            use_container_width=True,
                            key=f"dl_{fpath.name}",   # unique key per button
                        )

    # ─────────────────────────────────────────────────────────────────────────────
    #  1. NAČÍTANIE DÁT Z GRIB
    # ─────────────────────────────────────────────────────────────────────────────
    st.header("1. Načítanie a príprava meteorologických dát")
    st.markdown(
        """
        Použili sme reanalytické dáta **ERA5** od ECMWF vo formáte GRIB.
        Pre každú z 20 európskych krajín sme vyrezali priestorový výsek (bounding box)
        a uložili ho ako NetCDF súbor — zvlášť pre **meteorológiu** a **solárne dáta**.

        Vstupné premenné:

        | Premenná | Popis |
        |----------|-------|
        | `u100`   | Zložka vetra západ–východ vo výške 100 m |
        | `v100`   | Zložka vetra juh–sever vo výške 100 m |
        | `t2m`    | Teplota vzduchu vo výške 2 m (K) |
        | `sp`     | Tlak pri povrchu (Pa) |
        | `d2m`    | Rosný bod vo výške 2 m (K) |
        | `tcc`    | Pokrytie oblohy oblakmi (0–1) |

        > Výška 100 m zodpovedá typickej výške osi moderných veterných turbín.
        """
    )

    code_block("""\
    import cfgrib
    import xarray as xr

    regions = {
        'slovakia':    dict(latitude=slice(50.0, 47.5), longitude=slice(16.5, 22.5)),
        'czechia':     dict(latitude=slice(51.5, 48.5), longitude=slice(12.5, 18.5)),
        'poland':      dict(latitude=slice(55.0, 49.0), longitude=slice(14.0, 24.5)),
        'germany':     dict(latitude=slice(55.5, 47.0), longitude=slice(6.0,  15.0)),
        'france':      dict(latitude=slice(51.5, 42.0), longitude=slice(-5.0,  8.5)),
        'spain':       dict(latitude=slice(44.0, 36.0), longitude=slice(-9.5,  4.5)),
        'italy':       dict(latitude=slice(47.5, 37.5), longitude=slice(6.5,  18.5)),
        'austria':     dict(latitude=slice(49.0, 46.5), longitude=slice(9.5,  17.5)),
        'hungary':     dict(latitude=slice(48.5, 45.5), longitude=slice(16.0, 23.0)),
        'romania':     dict(latitude=slice(48.5, 43.5), longitude=slice(21.5, 30.0)),
        # ... (ďalšie krajiny)
    }

    print("Opening GRIB file...")
    datasets = cfgrib.open_datasets('./34dfd9df1905abfe67d03cc820043f8a.grib')
    ds0 = datasets[0]   # sp, tcc, t2m, d2m, u100, v100, ...
    ds1 = datasets[1]   # ssrd, cdir

    for name, bbox in regions.items():
        print(f"Processing {name}...")
        r0 = ds0.sel(**bbox).load()
        r1 = ds1.sel(**bbox).load()
        r0.to_netcdf(f'{name}_weather_2025.nc')
        r1.to_netcdf(f'{name}_solar_2025.nc')
        del r0, r1
        print(f"  Saved {name}_weather_2025.nc + {name}_solar_2025.nc")

    print("All done!")
    """)

    st.divider()

    # ─────────────────────────────────────────────────────────────────────────────
    #  2. NAČÍTANIE DO NUMPY
    # ─────────────────────────────────────────────────────────────────────────────
    st.header("2. Načítanie dát do NumPy poľa")
    st.markdown(
        """
        NetCDF súbor pre Slovensko načítame cez `xarray` a prevedieme na NumPy tenzor
        tvaru **(8 760, 11, 25, 6)** — 8 760 hodín × 11 zemepisných šírok × 25 dĺžok × 6 premenných.
        Cieľová premenná `y` je hodinová výroba vetra v GW načítaná z Excelu.
        """
    )

    code_block("""\
    import numpy as np
    import xarray as xr

    ds = xr.open_dataset('slovakia/slovakia_weather_2025.nc', decode_timedelta=False)

    vars = ['u100', 'v100', 't2m', 'sp', 'd2m', 'tcc']
    ds = ds[vars]

    # shape: (time, lat, lon, features)
    X = np.stack([ds[v].values for v in vars], axis=-1)
    print(f"X shape: {X.shape}")   # → (8760, 11, 25, 6)
    """)

    code_block("""\
    import pandas as pd

    df = pd.read_excel('slovakia/2025.xlsx')
    df['Date (GMT+1)'] = pd.to_datetime(df['Date (GMT+1)'])
    df = df.set_index('Date (GMT+1)')
    y = df['Wind onshore'].to_numpy()   # GW
    """)

    st.divider()

    # ─────────────────────────────────────────────────────────────────────────────
    #  3. PREDSPRACOVANIE
    # ─────────────────────────────────────────────────────────────────────────────
    st.header("3. Predspracovanie — škálovanie a rozdelenie dát")
    st.markdown(
        """
        Správny postup je:
        1. Odstrániť NaN hodnoty,
        2. rozdeliť dáta na trénovaciu (80 %) a testovaciu (20 %) sadu **pred škálovaním**,
        3. `StandardScaler` (X) a `MinMaxScaler` (y) fitovať **iba na trénovacích dátach**
        a následne transformovať testovacie — tým predchádzame úniku informácií (*data leakage*).
        """
    )

    code_block("""\
    from sklearn.preprocessing import StandardScaler, MinMaxScaler

    # 1 — Fix NaNs
    X = np.nan_to_num(X, nan=0.0)
    mask = ~np.isnan(y)
    X, y = X[mask], y[mask]

    # 2 — Chronologický split (nie náhodný — ide o časový rad!)
    n = len(X)
    split = int(0.8 * n)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # 3 — Škálovanie X (fit len na train)
    scaler = StandardScaler()
    X_train_flat = scaler.fit_transform(X_train.reshape(len(X_train), -1))
    X_test_flat  = scaler.transform(X_test.reshape(len(X_test), -1))
    X_train = X_train_flat.reshape(len(X_train), 11, 25, 6)
    X_test  = X_test_flat.reshape(len(X_test),  11, 25, 6)

    # 4 — Škálovanie y (fit len na train)
    y_scaler = MinMaxScaler()
    y_train_scaled = y_scaler.fit_transform(y_train.reshape(-1, 1)).flatten()
    y_test_scaled  = y_scaler.transform(y_test.reshape(-1, 1)).flatten()

    print(f"Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"y_train range: {y_train_scaled.min():.3f} – {y_train_scaled.max():.3f}")
    """)

    st.divider()

    # ─────────────────────────────────────────────────────────────────────────────
    #  4. POMOCNÉ FUNKCIE
    # ─────────────────────────────────────────────────────────────────────────────
    st.header("4. Pomocné funkcie — vyhodnotenie a vizualizácia")
    st.markdown(
        """
        `evaluate()` vypočíta **RMSE** a **MAE** na testovacej sade.
        `plot_model_results()` vykreslí trénovacie krivky a porovnanie predikcií so skutočnosťou.
        """
    )

    code_block("""\
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_squared_error, mean_absolute_error

    def evaluate(name, model, X_te, y_te):
        pred = model.predict(X_te).flatten()
        rmse = np.sqrt(mean_squared_error(y_te, pred))
        mae  = mean_absolute_error(y_te, pred)
        print(f"\\n{name}")
        print(f"  RMSE: {rmse:.4f} GW")
        print(f"  MAE:  {mae:.4f} GW")
        return pred

    def plot_model_results(name, history, y_true, y_pred):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4))
        fig.suptitle(f'Model: {name}', fontsize=14, fontweight='bold')

        axes[0].plot(history.history['loss'],     label='Train Loss')
        axes[0].plot(history.history['val_loss'], label='Val Loss')
        axes[0].set_title('Loss (MSE)'); axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('MSE');       axes[0].legend(); axes[0].grid(True)

        axes[1].plot(history.history['mae'],     label='Train MAE')
        axes[1].plot(history.history['val_mae'], label='Val MAE')
        axes[1].set_title('MAE'); axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('GW'); axes[1].legend(); axes[1].grid(True)

        axes[2].plot(y_true[:200], label='Actual',    alpha=0.8)
        axes[2].plot(y_pred[:200], label='Predicted', alpha=0.8)
        axes[2].set_title('Predictions vs Actual (first 200h)')
        axes[2].set_xlabel('Hour'); axes[2].set_ylabel('GW')
        axes[2].legend(); axes[2].grid(True)

        plt.tight_layout()
        plt.show()
    """)

    st.divider()

    # ─────────────────────────────────────────────────────────────────────────────
    #  5. MODELY
    # ─────────────────────────────────────────────────────────────────────────────
    st.header("5. Modely neurónových sietí")

    # ── MLP ───────────────────────────────────────────────────────────────────────
    with st.expander("🔷 MLP – Multilayer Perceptron", expanded=True):
        st.markdown(
            """
            Klasická plne prepojená sieť. Vstup je sploštený na 1D vektor (11 × 25 × 6 = 1 650 hodnôt).
            Sieť má len 2 skryté vrstvy — jednoduchosť je zámerná, slúži ako **základná línia (baseline)**.
            Trénovaná s `EarlyStopping(patience=30)` a maximom 50 epôch.
            """
        )
        code_block("""\
    from tensorflow import keras
    from tensorflow.keras import layers

    X_train_flat = X_train.reshape(len(X_train), -1)   # (n, 1650)
    X_test_flat  = X_test.reshape(len(X_test),  -1)

    mlp = keras.Sequential([
        layers.Input(shape=(11*25*6,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1)
    ], name='MLP')

    mlp.compile(optimizer='adam', loss='mse', metrics=['mae'])
    mlp.summary()

    history_mlp = mlp.fit(
        X_train_flat, y_train_scaled,
        validation_split=0.1,
        epochs=50,
        batch_size=64,
        callbacks=[keras.callbacks.EarlyStopping(patience=30, restore_best_weights=True)],
        verbose=1
    )

    pred_mlp = evaluate('MLP', mlp, X_test_flat, y_test_scaled)
    plot_model_results('MLP', history_mlp, y_test_scaled, pred_mlp)
    """)
        # img("pages/images/output_10_6.png", caption="MLP – trénovacie krivky a predikcie")
        # st.markdown(
        #     """
        #     **Výsledok:** MLP sa trénoval stabilne. Validačná chyba je vyššia ako trénovacia
        #     (mierne pretrénovanie), no napriek tomu dosiahol **najlepšie výsledky** zo všetkých modelov.
        #     """
        # )

    # ── CNN ───────────────────────────────────────────────────────────────────────
    with st.expander("🔷 CNN – Convolutional Neural Network", expanded=True):
        st.markdown(
            """
            Konvolučná sieť pracuje so **2D priestorovou mriežkou** (11 × 25) ako s obrázkom s 6 kanálmi.
            Konvolučné filtre zachytávajú lokálne priestorové vzorce (frontálne systémy, orografické efekty).
            `EarlyStopping(patience=5)` zastavil tréning po 7 epochách.
            """
        )
        code_block("""\
    cnn = keras.Sequential([
        layers.Input(shape=(11, 25, 6)),
        layers.Conv2D(32,  (3, 3), activation='relu', padding='same'),
        layers.Conv2D(64,  (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.GlobalAveragePooling2D(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1)
    ], name='CNN')

    cnn.compile(optimizer='adam', loss='mse', metrics=['mae'])
    cnn.summary()

    history_cnn = cnn.fit(
        X_train, y_train_scaled,
        validation_split=0.1,
        epochs=50,
        batch_size=64,
        callbacks=[keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)],
        verbose=1
    )

    pred_cnn = evaluate('CNN', cnn, X_test, y_test_scaled)
    plot_model_results('CNN', history_cnn, y_test_scaled, pred_cnn)
    """)
        # img("pages/images/output_11_6.png", caption="CNN – trénovacie krivky a predikcie")
        # st.markdown(
        #     """
        #     **Výsledok:** CNN sa trénoval rýchlo a stabilne. Predikcie sú plynulejšie ako u MLP,
        #     no model ignoruje časovú postupnosť — nedokáže reagovať na rýchle výkyvy výroby.
        #     """
        # )

    # ── CNN+LSTM ──────────────────────────────────────────────────────────────────
    # with st.expander("🔷 CNN+LSTM – Hybridný model", expanded=True):
    #     st.markdown(
    #         """
    #         Hybridná architektúra kombinuje oba prístupy:
    #         - `TimeDistributed(Conv2D)` extrahuje **priestorové príznaky** z každého časového kroku,
    #         - `LSTM` spracuje výslednú sekvenciu a zachytí **časové závislosti**.

    #         Vstup je sekvencia 24 po sebe idúcich hodín (`SEQ_LEN = 24`).
    #         """
    #     )
    #     code_block("""\
    # SEQ_LEN = 24

    # def make_sequences(X, y, seq_len):
    #     Xs, ys = [], []
    #     X_f = X.reshape(len(X), -1)
    #     for i in range(seq_len, len(X)):
    #         Xs.append(X_f[i-seq_len:i])
    #         ys.append(y[i])
    #     return np.array(Xs), np.array(ys)

    # y_scaled = np.concatenate([y_train_scaled, y_test_scaled])
    # X_scaled = np.concatenate([X_train, X_test])
    # X_seq, y_seq = make_sequences(X_scaled, y_scaled, SEQ_LEN)

    # split_seq = int(0.8 * len(X_seq))
    # X_seq_train, X_seq_test = X_seq[:split_seq], X_seq[split_seq:]
    # y_seq_train, y_seq_test = y_seq[:split_seq], y_seq[split_seq:]

    # # Architektúra CNN+LSTM
    # inp = layers.Input(shape=(SEQ_LEN, 11*25*6))
    # x   = layers.Reshape((SEQ_LEN, 11, 25, 6))(inp)
    # x   = layers.TimeDistributed(layers.Conv2D(32, (3,3), activation='relu', padding='same'))(x)
    # x   = layers.TimeDistributed(layers.GlobalAveragePooling2D())(x)
    # x   = layers.LSTM(64)(x)
    # x   = layers.Dense(32, activation='relu')(x)
    # out = layers.Dense(1)(x)

    # cnn_lstm = keras.Model(inp, out, name='CNN_LSTM')
    # cnn_lstm.compile(optimizer='adam', loss='mse', metrics=['mae'])
    # cnn_lstm.summary()

    # history_cnn_lstm = cnn_lstm.fit(
    #     X_seq_train, y_seq_train,
    #     validation_split=0.1,
    #     epochs=50,
    #     batch_size=32,
    #     callbacks=[keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)],
    #     verbose=1
    # )

    # pred_cnn_lstm = evaluate('CNN+LSTM', cnn_lstm, X_seq_test, y_seq_test)
    # plot_model_results('CNN_LSTM', history_cnn_lstm, y_seq_test, pred_cnn_lstm)
    # """)
    #     img("pages/images/output_13_6.png", caption="CNN+LSTM – trénovacie krivky a predikcie")
    #     st.markdown(
    #         """
    #         **Výsledok:** Trénovacia chyba klesala výrazne, no validačná stagnovála —
    #         signál pretrénovania. Model potrebuje viac trénovacích dát.
    #         """
    #     )

    # st.divider()

    # ─────────────────────────────────────────────────────────────────────────────
    #  6. ZÁVEREČNÉ POROVNANIE
    # ─────────────────────────────────────────────────────────────────────────────
    st.header("6. Záverečné porovnanie")

    code_block("""\
    print("\\n" + "="*40)
    print("FINAL COMPARISON")
    print("="*40)
    for name, pred, y_true in [
        ('MLP',      pred_mlp,      y_test_scaled),
        ('CNN',      pred_cnn,      y_test_scaled),
        ('LSTM',     pred_lstm,     y_seq_test),
        ('CNN+LSTM', pred_cnn_lstm, y_seq_test),
    ]:
        rmse = np.sqrt(mean_squared_error(y_true, pred))
        mae  = mean_absolute_error(y_true, pred)
        print(f"{name:10s} → RMSE: {rmse:.4f} GW  |  MAE: {mae:.4f} GW")
    """)

    st.code("""\
    ========================================
    FINAL COMPARISON
    ========================================
    MLP        → RMSE: 0.4635 GW  |  MAE: 0.3218 GW
    CNN        → RMSE: 0.5355 GW  |  MAE: 0.3821 GW
    LSTM       → RMSE: 0.5493 GW  |  MAE: 0.3849 GW
    CNN+LSTM   → RMSE: 0.5156 GW  |  MAE: 0.3699 GW""", language="text")

    code_block("""\
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(y_test[:200],         label='Actual',   linewidth=2, color='black')
    ax.plot(pred_mlp[:200],       label='MLP',      alpha=0.7)
    ax.plot(pred_cnn[:200],       label='CNN',      alpha=0.7)
    ax.plot(pred_lstm[:200],      label='LSTM',     alpha=0.7)
    ax.plot(pred_cnn_lstm[:200],  label='CNN+LSTM', alpha=0.7)
    ax.set_title('All Models vs Actual (first 200h)')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Wind Generation (GW)')
    ax.legend(); ax.grid(True)
    plt.tight_layout()
    plt.show()
    """)

    # img("pages/images/output_15_0.png", caption="Porovnanie všetkých modelov – prvých 200 hodín")

    # # ── Metrics table ──────────────────────────────────────────────────────────────
    # st.subheader("📋 Súhrnná tabuľka metrík")

    # results = pd.DataFrame({
    #     "Model":     ["MLP", "CNN", "LSTM", "CNN+LSTM"],
    #     "RMSE (GW)": [0.4635, 0.5355, 0.5493, 0.5156],
    #     "MAE (GW)":  [0.3218, 0.3821, 0.3849, 0.3699],
    # }).set_index("Model")

    # def highlight_best(s):
    #     return [
    #         "background-color: #d4edda; font-weight:bold" if v == s.min() else ""
    #         for v in s
    #     ]

    # st.dataframe(
    #     results.style.apply(highlight_best, axis=0).format("{:.4f}"),
    #     use_container_width=True,
    # )

    # st.markdown(
    #     """
    #     > 🟢 Zelená bunka = najlepšia hodnota v danom stĺpci.

    #     ### Kľúčové zistenia

    #     - **MLP** prekvapivo vyhral napriek jednoduchosti — pri agregovanej výrobe za celé Slovensko
    #     priestorová/časová štruktúra prináša menšiu výhodu.
    #     - **CNN** konvergoval rýchlo, ale bez pamäte na predchádzajúce hodiny mu unikajú dynamické zmeny.
    #     - **LSTM** potrebuje dlhšie sekvencie a väčší dataset na efektívne učenie sa sezónnych vzorov.
    #     - **CNN+LSTM** má najväčší potenciál — s viacročnými dátami by mohol prekonať MLP.

    #     ### Odporúčania pre ďalší vývoj

    #     1. Rozšíriť dataset na **viacero rokov** (napr. 2019–2024).
    #     2. Vyskúšať **Transformer / Temporal Fusion Transformer** architektúru.
    #     3. Implementovať **probabilistickú predikciu** (predikčné intervaly).
    #     4. Pridať **ensemble** kombináciu predikcií viacerých modelov.
    #     """
    # )

    # st.divider()
    # st.caption(
    #     "Dáta: ERA5 reanalýza (ECMWF) · Modely: TensorFlow / Keras · "
    #     "Metriky: RMSE, MAE na testovacej sade (rok 2025)"
    # )