"""Final assignment upload + results pages (report-first version)."""

from datetime import datetime, timezone
from typing import List, Dict, Any
import io

import streamlit as st
from firebase_admin import firestore
from utils.firebase_client import get_firebase_clients


COLLECTION_NAME = "final_assignment_submissions"
TOPIC_NAME = "Final assignment: Predikcia dopytu po elektrickej energii (Load)"


def _upload_files_to_bucket(bucket, submission_id: str, email: str, files) -> List[Dict[str, Any]]:
    uploaded_files = []
    email_sanitized = email.replace("@", "_at_").replace(".", "_")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    for file in files:
        storage_path = f"final_assignments/{email_sanitized}/{submission_id}/{timestamp}_{file.name}"
        blob = bucket.blob(storage_path)
        blob.upload_from_file(file, content_type=file.type)
        uploaded_files.append(
            {
                "name": file.name,
                "content_type": file.type,
                "size": file.size,
                "storage_path": storage_path,
            }
        )
    return uploaded_files


def final_assignment_brief_page():
    st.title("Záverečné zadanie – pokyny")
    st.info("Odovzdanie: odborná správa + Jupyter notebook.")

    st.markdown(
        """
### Cieľ zadania
Vašou úlohou je navrhnúť, implementovať a porovnať modely na predikciu hodinového dopytu po elektrickej energii (**Load**)
na základe historických energetických dát a meteorologických premenných (teplota).

### Dáta
Základné dáta si viete stiahnuť na stránke:
""")
    
    st.link_button("Dáta", disabled=False, url="/zaverecne-zadanie-ziskanie-dat" )

    st.markdown("""
### Obdobie a rozdelenie dát
- **Tréningové obdobie:** 2022-01-01 až 2024-12-31
- **Testovacie obdobie:** 2025-01-01 až 2025-12-31

Pracujte s hodinovými dátami.

### Predikčný režim
- Použite prístup **sliding window**
- **Horizont predikcie:** nasledujúci týždeň (t. j. **168 hodín**)

V reporte stručne uveďte:
- akú veľkosť vstupného okna používate (lookback),
- aký krok posunu okna používate (step).

### Povinné modely
- **Linear Regression**
- **XGBoost**

### Ďalšie modely
Implementujte minimálne **2 ďalšie modely** podľa vlastného výberu  
(napr. Random Forest, LightGBM, LSTM, SVR alebo iné).

### Vyhodnotenie
Modely porovnajte pomocou metrík:
- **MSE**
- **RMSE**
- **MAPE**

Výsledky uveďte pre testovacie obdobie 2025 (odporúčane aj v tabuľke).

### Pridanie nových premenných (povinné)
Porovnajte výsledky:
1. **pred** pridaním nových premenných,
2. **po** pridaní nových premenných.

Následne krátko okomentujte, či sa výsledky zlepšili a prečo.

Príklady nových premenných:
- oneskorené hodnoty Load (lagy),
- kĺzavé priemery,
- časové premenné (hodina, deň v týždni, víkend),
- kombinácie s teplotou.

### Odovzdanie
1. **Odborná správa** v odporúčanom rozsahu **3–4 strany** (DOCX alebo PDF)
2. **Jupyter notebook** (`.ipynb`) s implementáciou
3. Voliteľné prílohy (grafy/obrázky)
4. Povinné uviesť: **študentský email** (v správe aj notebooku)
        """
    )

    st.subheader("Šablóna správy")
    st.write("Použite priloženú DOCX šablónu nižšie.")

    docx_template_path = "docs/sablona_zaverecne_zadanie.docx"
    try:
        with open(docx_template_path, "rb") as file:
            st.download_button(
                "Stiahnuť šablónu správy (DOCX)",
                data=file.read(),
                file_name="sablona_zaverecne_zadanie.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    except FileNotFoundError:
        st.warning("DOCX šablóna sa nenašla. Pridajte súbor do: docs/sablona_zaverecne_zadanie.docx")

def final_assignment_upload_page():
    st.title("Odovzdanie záverečného zadania")
    st.write("Nahrajte finálnu správu (PDF/DOCX) a notebook (.ipynb).")

    try:
        db, bucket = get_firebase_clients()
    except Exception as error:
        st.error("Odovzdanie je momentálne nedostupné (Firebase nie je nakonfigurovaný).")
        st.caption(f"Detail chyby: {error}")
        return

    with st.form("final_assignment_upload_form", clear_on_submit=False):
        email = st.text_input("Študentský email *", placeholder="meno.priezvisko@...").strip()
        full_name = st.text_input("Meno a priezvisko *").strip()
        country = st.text_input("Krajina *", placeholder="napr. Slovensko").strip()
        title = st.text_input("Názov práce *").strip()

        report_file = st.file_uploader(
            "Finálna správa (PDF alebo DOCX) *",
            type=["pdf", "docx"],
            accept_multiple_files=False,
        )
        notebook_file = st.file_uploader(
            "Jupyter notebook (.ipynb) *",
            type=["ipynb"],
            accept_multiple_files=False,
        )
        attachments = st.file_uploader(
            "Voliteľné prílohy (obrázky/grafy)",
            type=["png", "jpg", "jpeg", "webp", "pdf"],
            accept_multiple_files=True,
        )

        declaration = st.checkbox("Potvrdzujem, že správa má minimálne 5 strán. *")
        submitted = st.form_submit_button("Odoslať záverečné zadanie")

    if not submitted:
        return

    if not email or "@" not in email or "." not in email:
        st.error("Zadajte validný email.")
        return
    if not full_name:
        st.error("Doplňte meno a priezvisko.")
        return
    if not country:
        st.error("Doplňte krajinu.")
        return
    if not title:
        st.error("Doplňte názov práce.")
        return
    if report_file is None:
        st.error("Finálna správa (PDF/DOCX) je povinná.")
        return
    if notebook_file is None:
        st.error("Notebook (.ipynb) je povinný.")
        return
    if not declaration:
        st.error("Musíte potvrdiť minimálny rozsah 5 strán.")
        return

    submission_id = f"final-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    submitted_at = datetime.now(timezone.utc).isoformat()

    files_to_upload = [report_file, notebook_file] + (attachments or [])

    try:
        uploaded_files = _upload_files_to_bucket(bucket, submission_id, email, files_to_upload)

        payload = {
            "submission_id": submission_id,
            "topic": TOPIC_NAME,
            "email": email,
            "full_name": full_name,
            "country": country,
            "title": title,
            "submitted_at": submitted_at,
            "report_format": report_file.name.split(".")[-1].lower(),
            "declared_min_5_pages": True,
            "files": uploaded_files,
        }

        db.collection(COLLECTION_NAME).document(submission_id).set(payload)

        st.success("Zadanie bolo úspešne odovzdané.")
        st.write(f"ID odovzdania: {submission_id}")

    except Exception as error:
        st.error(f"Chyba pri odovzdaní: {error}")


def final_assignment_results_page():
    st.title("Prehľad finálnych odovzdaní")
    st.write("Zborník odovzdaných záverečných prác.")

    try:
        db, bucket = get_firebase_clients()
    except Exception as error:
        st.error("Zobrazenie je vypnuté, pretože Firebase nie je nakonfigurovaný.")
        st.caption(f"Detail chyby: {error}")
        return

    try:
        docs = (
            db.collection(COLLECTION_NAME)
            .order_by("submitted_at", direction=firestore.Query.DESCENDING)
            .limit(100)
            .stream()
        )
    except Exception as error:
        st.error(f"Chyba pri čítaní z Firestore: {error}")
        return

    records = [doc.to_dict() for doc in docs]
    if not records:
        st.caption("Zatiaľ nie sú žiadne odovzdania.")
        return

    for payload in records:
        with st.container(border=True):
            st.subheader(payload.get("title", "Bez názvu"))
            st.write(f"Autor: {payload.get('full_name', '')}")
            st.write(f"Email: {payload.get('email', '')}")
            st.write(f"Krajina: {payload.get('country', '')}")
            st.write(f"Čas odovzdania: {payload.get('submitted_at', '')}")
            st.write(f"ID: {payload.get('submission_id', '')}")

            st.markdown("**Súbory:**")
            for file_info in payload.get("files", []):
                file_name = file_info.get("name", "")
                storage_path = file_info.get("storage_path", "")
                st.write(f"- {file_name}")

                # Náhľad obrázkov
                if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and storage_path:
                    try:
                        blob = bucket.blob(storage_path)
                        image_bytes = blob.download_as_bytes()
                        st.image(image_bytes, caption=file_name)
                    except Exception as error:
                        st.error(f"Chyba pri načítaní obrázka {file_name}: {error}")