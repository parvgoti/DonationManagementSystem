import tempfile
import unittest
from pathlib import Path

from modules.storage import initialize_storage, donors_path, donations_path
from modules.donor import add_donor, get_all_donors
from modules.donation import add_donation, get_all_donations


class TestStorage(unittest.TestCase):
    def test_initialize_and_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            initialize_storage(base)

            self.assertTrue(donors_path(base).exists())
            self.assertTrue(donations_path(base).exists())

            donor = {
                "donor_id": "DTEST",
                "name": "Test User",
                "phone": "9876543210",
                "email": "test@example.com",
                "city": "Ahmedabad",
                "donor_type": "Individual",
            }
            add_donor(base, donor)
            self.assertEqual(len(get_all_donors(base)), 1)

            donation = {
                "donation_id": "DNTEST",
                "donor_id": "DTEST",
                "date": "2026-10-07",
                "amount": "2500",
                "cause": "Education",
                "source": "Individual",
                "payment_mode": "UPI",
                "description": "Test donation",
            }
            add_donation(base, donation)
            self.assertEqual(len(get_all_donations(base)), 1)


if __name__ == "__main__":
    unittest.main()
