"""
Streamlit dashboard for OneClickQuiz.
Run with:
    streamlit run frontend/app.py
Requires the API running locally on http://127.0.0.1:8000 (default) or set API_URL env/field.
"""

import os
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


DEFAULT_API = os.environ.get("API_URL", "http://127.0.0.1:8000")


def api_get(path: str, api_base: str, params: Optional[Dict[str, Any]] = None) -> Any:
    resp = requests.get(f"{api_base.rstrip('/')}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def api_post(path: str, api_base: str, json: Dict[str, Any]) -> Any:
    resp = requests.post(f"{api_base.rstrip('/')}{path}", json=json, timeout=60)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=15)
def load_jobs(api_base: str, status: Optional[str]) -> List[Dict[str, Any]]:
    params = {"status": status} if status else None
    return api_get("/jobs", api_base, params=params)


@st.cache_data(ttl=15)
def load_job_detail(api_base: str, job_id: str) -> Dict[str, Any]:
    return api_get(f"/jobs/{job_id}", api_base)


@st.cache_data(ttl=10)
def load_metrics(api_base: str) -> Dict[str, Any]:
    return api_get("/metrics", api_base)


def create_job_view(api_base: str):
    st.subheader("Créer un job")
    with st.form("create_job"):
        subject = st.text_input("Sujet", "La photosynthèse")
        level_choice = st.selectbox(
            "Niveau / cours",
            ["Terminale", "Première", "Seconde", "Collège", "Licence", "Master", "Doctorat", "Autre (saisie libre)"],
            index=0,
        )
        level = st.text_input("Saisie libre (si Autre)", "") if "Autre" in level_choice else level_choice
        language = st.selectbox("Langue", ["fr", "en"])
        count = st.slider("Nombre de MCQ", 1, 10, 1)
        submitted = st.form_submit_button("Générer")
        if submitted:
            try:
                data = api_post(
                    "/jobs/generate",
                    api_base,
                    {
                        "subject": subject,
                        "level": level,
                        "language": language,
                        "count": count,
                    },
                )
                st.success(f"Job {data['job']['job_id']} créé ({data['job']['status']})")
                st.json(data.get("items") or {})
            except Exception as e:  # noqa: BLE001
                st.error(f"Erreur: {e}")


def jobs_view(api_base: str):
    st.subheader("Jobs")
    status = st.selectbox("Filtre status", ["", "completed", "failed", "pending", "running"], index=0)
    try:
        jobs = load_jobs(api_base, status if status else None)
    except Exception as e:  # noqa: BLE001
        st.error(f"Erreur chargement jobs: {e}")
        return
    if not jobs:
        st.info("Aucun job.")
        return
    for j in jobs:
        with st.expander(f"{j['job_id']} · {j['subject']} · {j['status']}"):
            st.write(f"Niveau: {j['level']} · Langue: {j['language']} · Count: {j['count']}")
            if j.get("created_at"):
                st.write(f"Créé: {j['created_at']}")
            detail = None
            if st.button("Voir détail", key=f"detail-{j['job_id']}"):
                try:
                    detail = load_job_detail(api_base, j["job_id"])
                except Exception as e:  # noqa: BLE001
                    st.error(f"Erreur détail: {e}")
            if detail:
                items = detail.get("items") or []
                st.write(f"{len(items)} MCQ")
                for idx, m in enumerate(items, start=1):
                    st.markdown(f"**Q{idx}.** {m['question']}")
                    st.write("Options:", m["options"])
                    st.write(f"Réponse: {m['answer']}")
                    st.write(f"Bloom: {m['bloom']} · SOLO: {m['solo']} · Diff: {m['difficulty']}")
                export_url = f"{api_base}/jobs/{j['job_id']}/export?format=csv"
                st.markdown(f"[Exporter CSV]({export_url})")


def metrics_view(api_base: str):
    st.subheader("Métriques")
    try:
        metrics = load_metrics(api_base)
    except Exception as e:  # noqa: BLE001
        st.error(f"Erreur chargement métriques: {e}")
        return
    jobs = metrics.get("jobs", {})
    mcq = metrics.get("mcq", {})
    c1, c2, c3 = st.columns(3)
    c1.metric("Jobs total", jobs.get("total", 0))
    c2.metric("Jobs complétés", jobs.get("completed", 0))
    c3.metric("Jobs échoués", jobs.get("failed", 0))
    st.write(f"MCQ total: {mcq.get('total', 0)} · Moy/job: {jobs.get('avg_mcq_per_job')}")
    st.write(f"Dernier job: {jobs.get('latest_created_at')}")
    st.markdown(f"[Prometheus]({api_base}/metrics/prom)")
    st.json(metrics)


def main():
    st.set_page_config(page_title="OneClickQuiz Dashboard", layout="wide")
    st.title("OneClickQuiz Dashboard")

    with st.sidebar:
        st.header("Configuration")
        api_base = st.text_input("API URL", DEFAULT_API)
        if st.button("Rafraîchir caches"):
            load_jobs.clear()
            load_job_detail.clear()
            load_metrics.clear()
            st.success("Caches vidés.")

    tab1, tab2, tab3 = st.tabs(["Créer", "Jobs", "Métriques"])
    with tab1:
        create_job_view(api_base)
    with tab2:
        jobs_view(api_base)
    with tab3:
        metrics_view(api_base)


if __name__ == "__main__":
    main()
