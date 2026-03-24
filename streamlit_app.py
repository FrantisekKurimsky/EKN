import streamlit as st
import streamlit_nested_layout
from PIL import Image
from docs.cvicenie_7 import cvicenie_7
from docs.cvicenie_6 import cvicenie_6
from docs.cvicenie_8 import cvicenie_8
import pandas as pd
from datetime import datetime
import re
import hmac
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials, firestore, storage as firebase_storage
from problems import (
    math_problems_1,
    math_problems_2,
    math_problems_3,
)
from streamlit_pdf_viewer import pdf_viewer
import streamlit.components.v1 as components

st.set_page_config(layout="wide")


def _require_login_for_protected_pages() -> bool:
    auth_config = st.secrets.get("auth")
    if not auth_config or not auth_config.get("password"):
        st.error("Prihlasovanie nie je nastavene. Doplňte [auth] password do .streamlit/secrets.toml.")
        return False

    expected_password = str(auth_config["password"])
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False

    if st.session_state.is_authenticated:
        return True

    st.subheader("Prihlásenie")
    with st.form("protected_login_form"):
        password = st.text_input("Heslo", type="password")
        submitted = st.form_submit_button("Prihlásiť")

    if submitted:
        if hmac.compare_digest(password, expected_password):
            st.session_state.is_authenticated = True
            st.success("Prihlásenie úspešné.")
            st.rerun()
        else:
            st.error("Nesprávne heslo.")

    return False

def _safe_slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return cleaned.strip("_")[:80] or "student"


@st.cache_resource
def _get_firebase_clients():
    if "firebase" not in st.secrets:
        raise RuntimeError("Firebase nie je nakonfigurovany v .streamlit/secrets.toml.")

    firebase_config = st.secrets["firebase"]
    if "service_account" not in firebase_config:
        raise RuntimeError("Chyba sekcia [firebase.service_account] v secrets.")
    if "storage_bucket" not in firebase_config:
        raise RuntimeError("Chyba firebase.storage_bucket v secrets.")

    service_account_info = dict(firebase_config["service_account"])
    required_fields = [
        "type",
        "project_id",
        "private_key_id",
        "private_key",
        "client_email",
        "client_id",
        "token_uri",
    ]
    missing_fields = [field for field in required_fields if not service_account_info.get(field)]
    if missing_fields:
        raise RuntimeError(f"V secrets chybaju povinne Firebase polia: {', '.join(missing_fields)}")

    placeholder_markers = ["PASTE_FROM_SERVICE_ACCOUNT_JSON", "PASTE_KEY_HERE", "..."]
    for key, value in service_account_info.items():
        if isinstance(value, str) and any(marker in value for marker in placeholder_markers):
            raise RuntimeError(
                f"Pole firebase.service_account.{key} stale obsahuje placeholder hodnotu."
            )

    if "private_key" in service_account_info:
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")

    bucket_name = str(firebase_config["storage_bucket"]).strip()
    if bucket_name.startswith("gs://"):
        bucket_name = bucket_name[len("gs://"):]
    bucket_name = bucket_name.rstrip("/")
    if not bucket_name:
        raise RuntimeError("firebase.storage_bucket je prázdny.")

    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})

    db = firestore.client()
    bucket = firebase_storage.bucket()
    return db, bucket


def _save_uploaded_files(topic: str, result_title: str, description: str, files):
    db, bucket = _get_firebase_clients()
    timestamp = datetime.utcnow()
    submission_id = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    folder_prefix = f"submissions/{timestamp.strftime('%Y-%m-%d')}"

    uploaded_files = []
    for uploaded_file in files:
        blob_path = f"{folder_prefix}/{uploaded_file.name}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(
            uploaded_file.getvalue(),
            content_type=uploaded_file.type or "application/octet-stream",
        )

        uploaded_files.append(
            {
                "name": uploaded_file.name,
                "content_type": uploaded_file.type,
                "size_bytes": uploaded_file.size,
                "storage_path": blob_path,
            }
        )

    metadata = {
        "submission_id": submission_id,
        "topic": topic,
        "result_title": result_title,
        "description": description,
        "submitted_at": timestamp.isoformat(timespec="seconds") + "Z",
        "files": uploaded_files,
    }

    db.collection("student_submissions").document(submission_id).set(metadata)
    return metadata


def upload_results_page():
    st.title("Odovzdanie výsledkov")
    st.write("Táto stránka je určená na odovzdanie obrázkov výsledkov.")
    st.info("Dnešné témy: negatívne ceny na day-ahead trhu a lineárna regresia medzi residual load a cenou.")

    try:
        _get_firebase_clients()
    except Exception as error:
        st.error("Upload je momentálne vypnuty, pretoze Firebase nie je nakonfigurovany.")
        st.caption(f"Detail chyby: {error}")
        return

    with st.form("student_upload_form"):
        topic = st.selectbox(
            "Téma odovzdania",
            [
                "Negatívne ceny (day-ahead)",
                "Lineárna regresia (Residual Load vs Price)",
            ],
        )
        result_title = st.text_input("Názov výsledku")
        description = st.text_area("Popis výsledkov")
        files = st.file_uploader(
            "Nahrajte obrázky výsledkov",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True,
        )
        submitted = st.form_submit_button("Odoslať výsledky")

    if submitted:
        if not files:
            st.error("Nahrajte aspoň jeden obrázok.")
        elif not result_title.strip():
            st.error("Doplňte názov výsledku.")
        elif not description.strip():
            st.error("Doplňte krátky popis výsledkov.")
        else:
            submission_data = _save_uploaded_files(topic, result_title, description, files)
            st.success("Výsledky boli úspešne odoslané.")
            # st.write(f"ID odovzdania: {submission_data['submission_id']}")
            st.write("Nahrané súbory:")
            for uploaded_file in files:
                st.write(f"- {uploaded_file.name}")

    st.caption("Odovzdané výsledky nájdete v menu na stránke 'Prehľad výsledkov'.")


def view_results_page():
    st.title("Prehľad výsledkov")
    st.write("Zobrazenie odovzdaných výsledkov z Firebase.")

    try:
        db, bucket = _get_firebase_clients()
    except Exception as error:
        st.error("Zobrazenie je vypnuté, pretože Firebase nie je nakonfigurovaný.")
        st.caption(f"Detail chyby: {error}")
        return

    documents = (
        db.collection("student_submissions")
        .order_by("submitted_at", direction=firestore.Query.DESCENDING)
        .limit(50)
        .stream()
    )

    records = [doc.to_dict() for doc in documents]
    if not records:
        st.caption("Zatiaľ nie sú žiadne odovzdania.")
        return

    topics = sorted({payload.get("topic", "") for payload in records if payload.get("topic", "")})
    selected_topic = st.selectbox("Filter podľa témy", ["Všetky témy"] + topics)

    if selected_topic == "Všetky témy":
        filtered_records = records
    else:
        filtered_records = [payload for payload in records if payload.get("topic") == selected_topic]

    if not filtered_records:
        st.caption("Pre zvolenú tému nie sú žiadne odovzdania.")
        return

    st.caption(f"Počet zobrazených odovzdaní: {len(filtered_records)}")

    for payload in filtered_records:
        submission_id = payload.get("submission_id", "")
        topic = payload.get("topic", "")
        submitted_at = payload.get("submitted_at", "")
        result_title = payload.get("result_title", "Bez názvu")
        description = payload.get("description", "")
        files = payload.get("files", [])
        st.markdown("---")
        st.subheader(result_title)
        st.write(f"Téma: {topic}")
        st.write(f"Čas: {submitted_at}")
        # st.write(f"ID: {submission_id}")
        st.write(f"Popis: {description}")

        for file_info in files:
            file_name = file_info.get("name", "")
            storage_path = file_info.get("storage_path", "")
            if not storage_path:
                continue

            blob = bucket.blob(storage_path)
            image_bytes = blob.download_as_bytes()
            st.image(image_bytes, caption=file_name)



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
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Domov"
if "last_exercise_choice" not in st.session_state:
    st.session_state.last_exercise_choice = "Domov"

exercise_choice = st.sidebar.selectbox(
    "",
    exercise_pages,
    index=exercise_pages.index(st.session_state.last_exercise_choice),
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
    if st.sidebar.button("Odhlásiť"):
        st.session_state.is_authenticated = False
        st.rerun()

def home_page():
    st.title("Ekonomika v elektroenergetike")


    
def first(name, problems, number):
    

    st.title(name)

    slide_index = st.selectbox(
        "Príklad:",
        list(range(len(problems))),
        format_func=lambda x: f"Príklad: {number}.{x+1}"
    )
    
    
    # Display the current math problem and solution
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
            # st.write(example)
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
    home_page()
elif pages == "Cvičenie 1.":
    first("Cvičenie 1.", math_problems_1, 1)
elif pages == "Cvičenie 2.":
    first("Cvičenie 2.", math_problems_2, 2)
elif pages == "Cvičenie 3.":
    first("Cvičenie 3.", math_problems_3, 3)
elif pages == "Cvičenie 4. a 5.":
    st.title("Cvičenie 4. a 5.")
    pdf_viewer("docs/cv_4_5.pdf", width=800, pages_vertical_spacing=3, resolution_boost=2)
elif pages == "Cvičenie 6.":
    st.title("Cvičenie 6.")
    file_path = "docs/Cvicenie_6.ipynb"


    with open(file_path, "rb") as file:
        notebook_content = file.read()

    # Create a download button
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

    # Create a download button
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

    # Create a download button
    st.download_button(
        label="Stiahnuť Jupyter Notebook",
        data=notebook_content,
        file_name="Cvicenie_8.ipynb",
        mime="application/octet-stream"
    )
    cvicenie_8()
elif pages == "Odovzdanie výsledkov":
    if _require_login_for_protected_pages():
        upload_results_page()
elif pages == "Prehľad výsledkov":
    if _require_login_for_protected_pages():
        view_results_page()
