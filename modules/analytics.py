from pathlib import Path
import numpy as np
import pandas as pd


def donations_dataframe(donations):
    columns = [
        "donation_id", "donor_id", "date", "amount", "cause",
        "source", "payment_mode", "description"
    ]
    if not donations:
        return pd.DataFrame(columns=columns)

    df = pd.DataFrame(donations)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def get_summary_stats(donations):
    df = donations_dataframe(donations)

    if df.empty:
        return {
            "count": 0,
            "unique_donors": 0,
            "total": 0.0,
            "average": 0.0,
            "median": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
            "this_month": 0.0,
            "top_cause": "",
            "top_source": "",
        }

    now = pd.Timestamp.today()
    this_month = df[
        (df["date"].dt.year == now.year) &
        (df["date"].dt.month == now.month)
    ]["amount"].sum()

    cause_totals = df.groupby("cause")["amount"].sum().sort_values(ascending=False)
    source_totals = df.groupby("source")["amount"].sum().sort_values(ascending=False)

    amounts = df["amount"].to_numpy()

    return {
        "count": int(len(df)),
        "unique_donors": int(df["donor_id"].nunique()),
        "total": float(np.sum(amounts)),
        "average": float(np.mean(amounts)),
        "median": float(np.median(amounts)),
        "minimum": float(np.min(amounts)),
        "maximum": float(np.max(amounts)),
        "this_month": float(this_month),
        "top_cause": str(cause_totals.index[0]) if not cause_totals.empty else "",
        "top_source": str(source_totals.index[0]) if not source_totals.empty else "",
    }


def donations_by_cause(donations):
    df = donations_dataframe(donations)
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("cause")["amount"].sum().sort_values(ascending=False)


def donations_by_source(donations):
    df = donations_dataframe(donations)
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("source")["amount"].sum().sort_values(ascending=False)


def donations_by_month(donations):
    df = donations_dataframe(donations)
    if df.empty:
        return pd.Series(dtype=float)

    clean = df.dropna(subset=["date"]).copy()
    if clean.empty:
        return pd.Series(dtype=float)

    monthly = clean.groupby(
        clean["date"].dt.to_period("M")
    )["amount"].sum()

    monthly.index = monthly.index.astype(str)
    return monthly


def top_donor(donations, donors):
    df = donations_dataframe(donations)
    if df.empty:
        return None

    totals = df.groupby("donor_id")["amount"].sum().sort_values(ascending=False)
    donor_id = totals.index[0]

    donor_lookup = {d["donor_id"]: d for d in donors}
    donor = donor_lookup.get(donor_id, {})
    return {
        "donor_id": donor_id,
        "name": donor.get("name", donor_id),
        "total": float(totals.iloc[0]),
    }


get_top_donor = top_donor
