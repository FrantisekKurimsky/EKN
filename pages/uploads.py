"""Upload and results pages for student submissions."""
import streamlit as st
from firebase_admin import firestore
from utils.firebase_client import get_firebase_clients
from utils.submissions import save_uploaded_files


def upload_page():
    """Page for uploading results."""
    st.title("Odovzdanie výsledkov")
    st.write("Táto stránka je určená na odovzdanie obrázkov výsledkov.")
    st.info("Dnešné témy: Predicia výroby veternej energie")

    try:
        get_firebase_clients()
    except Exception as error:
        st.error("Upload je momentálne vypnuty, pretoze Firebase nie je nakonfigurovany.")
        st.caption(f"Detail chyby: {error}")
        return

    with st.form("student_upload_form"):
        topic = st.selectbox(
            "Téma odovzdania",
            [
                "Predicia výroby veternej energie",
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
            try:
                submission_data = save_uploaded_files(topic, result_title, description, files)
                st.success("Výsledky boli úspešne odoslané.")
                st.write(f"ID odovzdania: {submission_data['submission_id']}")
                st.write("Nahrané súbory:")
                for uploaded_file in files:
                    st.write(f"- {uploaded_file.name}")
            except Exception as error:
                st.error(f"Chyba pri uploade: {error}")

    st.caption("Odovzdané výsledky nájdete v menu na stránke 'Prehľad výsledkov'.")


def results_page():
    """Page for viewing submitted results with topic filter."""
    st.title("Prehľad výsledkov")
    st.write("Zobrazenie odovzdaných výsledkov z Firebase.")

    try:
        db, bucket = get_firebase_clients()
    except Exception as error:
        st.error("Zobrazenie je vypnuté, pretože Firebase nie je nakonfigurovaný.")
        st.caption(f"Detail chyby: {error}")
        return

    try:
        documents = (
            db.collection("student_submissions")
            .order_by("submitted_at", direction=firestore.Query.DESCENDING)
            .limit(50)
            .stream()
        )
    except Exception as error:
        st.error(f"Chyba pri čítaní z Firestore: {error}")
        return

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

    for row_start in range(0, len(filtered_records), 2):
        row_items = filtered_records[row_start:row_start + 2]
        cols = st.columns(2, gap="large")

        for col_index, payload in enumerate(row_items):
            submission_id = payload.get("submission_id", "")
            topic = payload.get("topic", "")
            submitted_at = payload.get("submitted_at", "")
            result_title = payload.get("result_title", "Bez názvu")
            description = payload.get("description", "")
            files = payload.get("files", [])

            with cols[col_index]:
                with st.container(border=True):
                    st.subheader(result_title)
                    st.write(f"Téma: {topic}")
                    st.write(f"Čas: {submitted_at}")
                    st.write(f"ID: {submission_id}")
                    st.write(f"Popis: {description}")

                    for file_info in files:
                        file_name = file_info.get("name", "")
                        storage_path = file_info.get("storage_path", "")
                        if not storage_path:
                            continue

                        try:
                            blob = bucket.blob(storage_path)
                            image_bytes = blob.download_as_bytes()
                            st.image(image_bytes, caption=file_name)
                        except Exception as error:
                            st.error(f"Chyba pri načítavaní obrázka {file_name}: {error}")
