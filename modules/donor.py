from modules.storage import donors_path, DONOR_COLUMNS, read_records, write_records


def get_all_donors(base_dir):
    return read_records(donors_path(base_dir), DONOR_COLUMNS)


def add_donor(base_dir, donor):
    donors = get_all_donors(base_dir)
    if any(d["donor_id"] == donor["donor_id"] for d in donors):
        raise ValueError("Donor ID already exists.")
    donors.append(donor)
    write_records(donors_path(base_dir), DONOR_COLUMNS, donors)


def update_donor(base_dir, donor_id, updated_donor):
    donors = get_all_donors(base_dir)
    found = False
    for index, donor in enumerate(donors):
        if donor["donor_id"] == donor_id:
            donors[index] = updated_donor
            found = True
            break
    if found:
        write_records(donors_path(base_dir), DONOR_COLUMNS, donors)
    return found


def delete_donor(base_dir, donor_id):
    donors = get_all_donors(base_dir)
    remaining = [d for d in donors if d["donor_id"] != donor_id]
    if len(remaining) == len(donors):
        return False
    write_records(donors_path(base_dir), DONOR_COLUMNS, remaining)
    return True


def search_donors(base_dir, query):
    query = str(query).strip().lower()
    donors = get_all_donors(base_dir)
    if not query:
        return donors

    results = []
    for donor in donors:
        combined = " ".join(donor.values()).lower()
        if query in combined:
            results.append(donor)
    return results
