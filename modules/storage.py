import csv
from pathlib import Path

DONOR_COLUMNS = ["donor_id", "name", "phone", "email", "city", "donor_type"]
DONATION_COLUMNS = [
    "donation_id", "donor_id", "date", "amount", "cause",
    "source", "payment_mode", "description"
]


def data_dir(base_dir):
    return Path(base_dir) / "data"


def donors_path(base_dir):
    return data_dir(base_dir) / "donors.csv"


def donations_path(base_dir):
    return data_dir(base_dir) / "donations.csv"


def ensure_csv(path, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()


def initialize_storage(base_dir):
    ensure_csv(donors_path(base_dir), DONOR_COLUMNS)
    ensure_csv(donations_path(base_dir), DONATION_COLUMNS)


def read_records(path, columns):
    ensure_csv(path, columns)
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_records(path, columns, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)
