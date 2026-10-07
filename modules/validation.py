import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _required(value, field_name):
    if value is None or str(value).strip() == "":
        return False, f"{field_name} is required."
    return True, ""


def validate_donor(data):
    required_fields = {
        "donor_id": "Donor ID",
        "name": "Name",
        "phone": "Phone",
        "city": "City",
        "donor_type": "Donor Type",
    }
    for key, label in required_fields.items():
        ok, msg = _required(data.get(key), label)
        if not ok:
            return False, msg

    phone = str(data["phone"]).strip()
    if not phone.isdigit() or not (10 <= len(phone) <= 15):
        return False, "Phone must contain 10 to 15 digits."

    email = str(data.get("email", "")).strip()
    if email and not EMAIL_RE.match(email):
        return False, "Please enter a valid email address."

    return True, ""


def validate_donation(data):
    required_fields = {
        "donation_id": "Donation ID",
        "donor_id": "Donor ID",
        "date": "Date",
        "amount": "Amount",
        "cause": "Cause",
        "source": "Source",
        "payment_mode": "Payment Mode",
    }
    for key, label in required_fields.items():
        ok, msg = _required(data.get(key), label)
        if not ok:
            return False, msg

    try:
        amount = float(data["amount"])
    except (TypeError, ValueError):
        return False, "Amount must be a valid number."

    if amount <= 0:
        return False, "Amount must be greater than 0."

    try:
        datetime.strptime(str(data["date"]).strip(), "%Y-%m-%d")
    except ValueError:
        return False, "Date must use YYYY-MM-DD format."

    return True, ""


def validate_search_amount(value):
    if value is None or str(value).strip() == "":
        return True, ""
    try:
        amount = float(value)
        if amount < 0:
            return False, "Search amount cannot be negative."
        return True, ""
    except ValueError:
        return False, "Search amount must be numeric."
