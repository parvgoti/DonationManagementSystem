from modules.storage import donations_path, DONATION_COLUMNS, read_records, write_records


def get_all_donations(base_dir):
    return read_records(donations_path(base_dir), DONATION_COLUMNS)


def _normalize(record):
    record = record.copy()
    try:
        record["amount"] = f"{float(record['amount']):.2f}"
    except (TypeError, ValueError):
        pass
    return record


def add_donation(base_dir, donation):
    donations = get_all_donations(base_dir)
    if any(d["donation_id"] == donation["donation_id"] for d in donations):
        raise ValueError("Donation ID already exists.")
    donations.append(_normalize(donation))
    write_records(donations_path(base_dir), DONATION_COLUMNS, donations)


def update_donation(base_dir, donation_id, updated_donation):
    donations = get_all_donations(base_dir)
    found = False
    for index, donation in enumerate(donations):
        if donation["donation_id"] == donation_id:
            donations[index] = _normalize(updated_donation)
            found = True
            break
    if found:
        write_records(donations_path(base_dir), DONATION_COLUMNS, donations)
    return found


def delete_donation(base_dir, donation_id):
    donations = get_all_donations(base_dir)
    remaining = [d for d in donations if d["donation_id"] != donation_id]
    if len(remaining) == len(donations):
        return False
    write_records(donations_path(base_dir), DONATION_COLUMNS, remaining)
    return True


def search_donations(base_dir, query):
    query = str(query).strip().lower()
    donations = get_all_donations(base_dir)
    if not query:
        return donations

    results = []
    for donation in donations:
        combined = " ".join(donation.values()).lower()
        if query in combined:
            results.append(donation)
    return results
