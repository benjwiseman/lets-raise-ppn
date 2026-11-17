"""Nematode Culture Tracker: Streamlit dashboard (step 1 stub).

Loads the culture log, works out each pot's age and status, and shows a
table. The forecasting views are added in later steps.
"""
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data"
TERMINAL = {"final_harvest": "Harvested", "plant_died": "Died", "discarded": "Discarded"}

st.set_page_config(page_title="Nematode Culture Tracker", layout="wide")


@st.cache_data
def load():
    pots = pd.read_csv(DATA / "pots.csv", parse_dates=["seeded_date", "transplant_date", "inoculation_date"])
    events = pd.read_csv(DATA / "events.csv", parse_dates=["date"])
    return pots, events


def pot_status(pots: pd.DataFrame, events: pd.DataFrame, today: pd.Timestamp) -> pd.DataFrame:
    """Status comes from the event log, so it can never disagree with it."""
    out = pots.copy()
    ended = (events[events.event_type.isin(TERMINAL)]
             .sort_values("date").groupby("pot_id").last()[["event_type", "date"]])
    out = out.join(ended, on="pot_id")
    out["status"] = out["event_type"].map(TERMINAL).fillna("Active")
    end = out["date"].fillna(today)
    out["days_post_inoculation"] = (end - out["inoculation_date"]).dt.days
    harvests = events[events.event_type.isin(["partial_harvest", "final_harvest"])]
    out = out.join(harvests.groupby("pot_id").agg(harvests=("event_id", "count"),
                                                  eggs_harvested=("eggs_counted", "sum")), on="pot_id")
    out[["harvests", "eggs_harvested"]] = out[["harvests", "eggs_harvested"]].fillna(0).astype(int)
    out["simulated"] = out["pot_id"].str.startswith("SIM-")
    return out.drop(columns=["event_type", "date"])


pots, events = load()
today = pd.Timestamp(date.today())
status = pot_status(pots, events, today)

st.title("Nematode Culture Tracker")
if status["simulated"].any():
    st.warning("This dashboard is currently showing **simulated data** for development. "
               "It is not a record of real lab cultures.", icon="⚠️")

active = status[status.status == "Active"]
c1, c2, c3 = st.columns(3)
c1.metric("Active pots", len(active))
c2.metric("Ready (≥ 60 days post-inoculation)", int((active.days_post_inoculation >= 60).sum()))
c3.metric("Nematode species in culture", active.nematode_species.nunique())

st.subheader("All pots")
st.dataframe(
    status[["pot_id", "nematode_species", "host_species", "host_cultivar", "greenhouse",
            "inoculation_date", "inoculum_stage", "inoculum_count", "days_post_inoculation",
            "status", "harvests", "eggs_harvested"]],
    hide_index=True, use_container_width=True,
    column_config={"inoculation_date": st.column_config.DateColumn(format="YYYY-MM-DD")},
)
st.caption("Next steps: simulated harvest history, yield and survival models, harvest forecast.")
