"""Final assignment page: download and merge energy load with weather temperatures."""

from typing import Dict, Tuple
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

ENERGY_CHARTS_BASE = "https://api.energy-charts.info"

COUNTRY_MAP: Dict[str, str] = {
    "Slovensko": "sk",
    "Cesko": "cz",
    "Madarsko": "hu",
    "Nemecko": "de",
    "Francuzsko": "fr",
    "Spanielsko": "es",
    "Portugalsko": "pt",
    "Holandsko": "nl",
    "Belgicko": "be",
    "Polsko": "pl",
    "Rakusko": "at",
    "Slovinsko": "si",
    "Norsko": "no",
    "Svedsko": "se",
    "Dansko": "dk",
}

# Open-Meteo timezone podľa krajiny (aby sedeli časové osi)
OPENMETEO_TZ: Dict[str, str] = {
    "sk": "Europe/Bratislava",
    "cz": "Europe/Prague",
    "hu": "Europe/Budapest",
    "de": "Europe/Berlin",
    "fr": "Europe/Paris",
    "es": "Europe/Madrid",
    "pt": "Europe/Lisbon",
    "nl": "Europe/Amsterdam",
    "be": "Europe/Brussels",
    "pl": "Europe/Warsaw",
    "at": "Europe/Vienna",
    "si": "Europe/Ljubljana",
    "no": "Europe/Oslo",
    "se": "Europe/Stockholm",
    "dk": "Europe/Copenhagen",
}

CITY_OPTIONS: Dict[str, Dict[str, Tuple[float, float]]] = {
    "Slovensko": {
        "Bratislava": (48.1486, 17.1077),
        "Kosice": (48.7164, 21.2611),
        "Zilina": (49.2231, 18.7394),
        "Banska Bystrica": (48.7363, 19.1462),
        "Presov": (48.9984, 21.2393),
        "Nitra": (48.3064, 18.0764),
    },
    "Cesko": {
        "Praha": (50.0755, 14.4378),
        "Brno": (49.1951, 16.6068),
        "Ostrava": (49.8209, 18.2625),
        "Plzen": (49.7384, 13.3736),
        "Liberec": (50.7671, 15.0562),
        "Olomouc": (49.5938, 17.2509),
    },
    "Madarsko": {
        "Budapest": (47.4979, 19.0402),
        "Debrecen": (47.5316, 21.6273),
        "Szeged": (46.2530, 20.1414),
        "Miskolc": (48.1035, 20.7784),
        "Pecs": (46.0727, 18.2323),
        "Gyor": (47.6875, 17.6504),
    },
    "Nemecko": {
        "Berlin": (52.5200, 13.4050),
        "Hamburg": (53.5511, 9.9937),
        "Munich": (48.1351, 11.5820),
        "Cologne": (50.9375, 6.9603),
        "Frankfurt": (50.1109, 8.6821),
        "Leipzig": (51.3397, 12.3731),
    },
    "Francuzsko": {
        "Paris": (48.8566, 2.3522),
        "Lyon": (45.7640, 4.8357),
        "Marseille": (43.2965, 5.3698),
        "Toulouse": (43.6047, 1.4442),
        "Nice": (43.7102, 7.2620),
        "Lille": (50.6292, 3.0573),
    },
    "Spanielsko": {
        "Madrid": (40.4168, -3.7038),
        "Barcelona": (41.3874, 2.1686),
        "Valencia": (39.4699, -0.3763),
        "Seville": (37.3891, -5.9845),
        "Bilbao": (43.2630, -2.9350),
        "Zaragoza": (41.6488, -0.8891),
    },
    "Portugalsko": {
        "Lisbon": (38.7223, -9.1393),
        "Porto": (41.1579, -8.6291),
        "Braga": (41.5454, -8.4265),
        "Coimbra": (40.2033, -8.4103),
        "Faro": (37.0194, -7.9304),
        "Aveiro": (40.6405, -8.6538),
    },
    "Holandsko": {
        "Amsterdam": (52.3676, 4.9041),
        "Rotterdam": (51.9244, 4.4777),
        "The Hague": (52.0705, 4.3007),
        "Utrecht": (52.0907, 5.1214),
        "Eindhoven": (51.4416, 5.4697),
        "Groningen": (53.2194, 6.5665),
    },
    "Belgicko": {
        "Brussels": (50.8503, 4.3517),
        "Antwerp": (51.2194, 4.4025),
        "Ghent": (51.0543, 3.7174),
        "Liege": (50.6326, 5.5797),
        "Bruges": (51.2093, 3.2247),
        "Charleroi": (50.4108, 4.4446),
    },
    "Polsko": {
        "Warsaw": (52.2297, 21.0122),
        "Krakow": (50.0647, 19.9450),
        "Lodz": (51.7592, 19.4550),
        "Wroclaw": (51.1079, 17.0385),
        "Poznan": (52.4064, 16.9252),
        "Gdansk": (54.3520, 18.6466),
    },
    "Rakusko": {
        "Vienna": (48.2082, 16.3738),
        "Graz": (47.0707, 15.4395),
        "Linz": (48.3069, 14.2858),
        "Salzburg": (47.8095, 13.0550),
        "Innsbruck": (47.2692, 11.4041),
        "Klagenfurt": (46.6247, 14.3053),
    },
    "Slovinsko": {
        "Ljubljana": (46.0569, 14.5058),
        "Maribor": (46.5547, 15.6459),
        "Celje": (46.2397, 15.2677),
        "Kranj": (46.2389, 14.3556),
        "Koper": (45.5481, 13.7302),
        "Novo Mesto": (45.8030, 15.1689),
    },
    "Norsko": {
        "Oslo": (59.9139, 10.7522),
        "Bergen": (60.3913, 5.3221),
        "Trondheim": (63.4305, 10.3951),
        "Stavanger": (58.9700, 5.7331),
        "Tromso": (69.6492, 18.9553),
        "Drammen": (59.7439, 10.2045),
    },
    "Svedsko": {
        "Stockholm": (59.3293, 18.0686),
        "Gothenburg": (57.7089, 11.9746),
        "Malmo": (55.6050, 13.0038),
        "Uppsala": (59.8586, 17.6389),
        "Vasteras": (59.6111, 16.5448),
        "Orebro": (59.2741, 15.2066),
    },
    "Dansko": {
        "Copenhagen": (55.6761, 12.5683),
        "Aarhus": (56.1629, 10.2039),
        "Odense": (55.4038, 10.4024),
        "Aalborg": (57.0488, 9.9217),
        "Esbjerg": (55.4765, 8.4594),
        "Randers": (56.4606, 10.0364),
    },
}


def _normalize_city_col(city_name: str) -> str:
    return f"temp_{city_name.lower().replace(' ', '_')}"


@st.cache_data(show_spinner=False)
def fetch_energy_load(country_code: str, start_date: str, end_date: str, timezone_name: str) -> pd.DataFrame:
    """
    Energy Charts /public_power:
    - unix_seconds -> lokalny cas vybranej krajiny
    - z production_types berieme len 'Load'
    - final stlpce: Date, Load (hodinove)
    """
    url = f"{ENERGY_CHARTS_BASE}/public_power"
    params = {"country": country_code, "start": start_date, "end": end_date}
    response = requests.get(url, params=params, timeout=90)
    response.raise_for_status()
    data = response.json()

    if "unix_seconds" not in data or "production_types" not in data:
        raise ValueError("Neocakavany format response z /public_power.")

    unix_seconds = data["unix_seconds"]
    production_types = data["production_types"]

    load_series = None
    for item in production_types:
        name = str(item.get("name", "")).strip().lower()
        if name == "load":
            load_series = item.get("data", [])
            break

    if load_series is None:
        for item in production_types:
            if "load" in str(item.get("name", "")).lower():
                load_series = item.get("data", [])
                break

    if load_series is None:
        raise ValueError("V production_types sa nenasiel stlpec 'Load'.")

    # unix_seconds -> UTC -> lokalna timezone krajiny -> naive local datetime
    date_local = (
        pd.to_datetime(unix_seconds, unit="s", utc=True)
        .tz_convert(timezone_name)
        .tz_localize(None)
    )

    df = pd.DataFrame(
        {
            "Date": date_local,
            "Load": pd.to_numeric(load_series, errors="coerce"),
        }
    )

    # vstup byva 15-min; prevedieme na hodinove
    df = df.dropna(subset=["Date"]).sort_values("Date").set_index("Date")
    hourly = df.resample("1h").mean().interpolate(limit_direction="both").reset_index()
    return hourly[["Date", "Load"]]


@st.cache_data(show_spinner=False)
def fetch_openmeteo_hourly_temp(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str,
    timezone_name: str,
) -> pd.DataFrame:
    """
    Open-Meteo archive:
    - pytame v rovnakej timezone ako Energy Charts data pre dany stat
    - vraciame Date ako naive local datetime
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": timezone_name,
    }
    response = requests.get(url, params=params, timeout=90)
    response.raise_for_status()
    data = response.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])

    return pd.DataFrame(
        {
            "Date": pd.to_datetime(times, errors="coerce"),  # local naive
            "temperature_2m": pd.to_numeric(temps, errors="coerce"),
        }
    )


def final_assignment_data_page() -> None:
    st.title("Energy Load + Open-Meteo teploty (2022-2025)")
    st.caption(f"Posledna aktualizacia: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    country_name = st.selectbox("Vyber stat", list(COUNTRY_MAP.keys()), index=0)
    country_code = COUNTRY_MAP[country_name]
    timezone_name = OPENMETEO_TZ[country_code]

    st.write("Vyber minimalne 5 miest:")
    cities_available = list(CITY_OPTIONS[country_name].keys())
    selected_cities = st.multiselect("Mesta", options=cities_available, default=cities_available[:5])

    if len(selected_cities) < 5:
        st.warning("Prosim vyber aspon 5 miest.")
        return

    start_date = "2022-01-01"
    end_date = "2025-12-31"

    if st.button("Stiahnut a pripravit data", type="primary"):
        try:
            with st.spinner("Stahujem load data z Energy Charts (/public_power)..."):
                result = fetch_energy_load(country_code, start_date, end_date, timezone_name)

            with st.spinner("Stahujem hodinove teploty pre mesta z Open-Meteo..."):
                for city in selected_cities:
                    lat, lon = CITY_OPTIONS[country_name][city]
                    city_temp = fetch_openmeteo_hourly_temp(lat, lon, start_date, end_date, timezone_name)
                    city_col = _normalize_city_col(city)
                    city_temp = city_temp.rename(columns={"temperature_2m": city_col})
                    result = result.merge(city_temp, on="Date", how="left")

                temp_cols = [c for c in result.columns if c.startswith("temp_")]
                result["temp_avg"] = result[temp_cols].mean(axis=1)

            ordered_cols = ["Date", "Load"] + [c for c in result.columns if c.startswith("temp_")] + ["temp_avg"]
            ordered_cols = list(dict.fromkeys(ordered_cols))
            result = result[ordered_cols].sort_values("Date").reset_index(drop=True)

            st.success("Hotovo")
            st.subheader("Vysledny DataFrame")
            st.dataframe(result.head(50), width='stretch')
            st.write(f"Pocet riadkov: {len(result):,}")
            st.write(f"Stlpce: {list(result.columns)}")

            csv_data = result.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Stiahnut CSV",
                data=csv_data,
                file_name=f"energy_load_temp_{country_code}_2022_2025_hourly.csv",
                mime="text/csv",
            )

        except requests.RequestException as error:
            st.error(f"Chyba siete pri stahovani dat: {error}")
        except Exception as error:
            st.error(f"Chyba pri priprave dat: {error}")
