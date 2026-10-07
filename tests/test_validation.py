import unittest
from modules.validation import validate_donor, validate_donation


class TestValidation(unittest.TestCase):
    def test_valid_donor(self):
        data = {
            "donor_id": "D100",
            "name": "Test User",
            "phone": "9876543210",
            "email": "test@example.com",
            "city": "Ahmedabad",
            "donor_type": "Individual",
        }
        self.assertEqual(validate_donor(data)[0], True)

    def test_invalid_phone(self):
        data = {
            "donor_id": "D100",
            "name": "Test User",
            "phone": "123",
            "email": "",
            "city": "Ahmedabad",
            "donor_type": "Individual",
        }
        self.assertFalse(validate_donor(data)[0])

    def test_invalid_amount(self):
        data = {
            "donation_id": "DN100",
            "donor_id": "D100",
            "date": "2026-10-07",
            "amount": "-20",
            "cause": "Education",
            "source": "Individual",
            "payment_mode": "UPI",
        }
        self.assertFalse(validate_donation(data)[0])


if __name__ == "__main__":
    unittest.main()
